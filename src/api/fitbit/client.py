import logging

import backoff
import requests

from api.fitbit.user import User

logger = logging.getLogger(__name__)


class Client:
    # WebAPI endpoint details
    _HOSTNAME: str = 'https://api.fitbit.com'
    _DEFAULT_API_VERSION: int = 1
    _OAUTH2_PATH: str = '/oauth2/token'
    _PROFILE_PATH: str = '/{}/user/{}/profile.json'

    # HTTP request timeout, retries
    _REQUEST_TIMEOUT: float = 5.0
    _REQUEST_RETRIES: int = 5

    # Request, Response data key/values
    _GRANT_TYPE_VALUE: str = 'refresh_token'
    _ACCESS_TOKEN_KEY: str = 'access_token'
    _REFRESH_TOKEN_KEY: str = 'refresh_token'

    def __init__(self,
                 api_version: int = _DEFAULT_API_VERSION) -> None:
        self.api_version = api_version

    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.ConnectionError,
                           requests.exceptions.Timeout),
                          logger=logger,
                          max_tries=_REQUEST_RETRIES
                          )
    def _refresh(self,
                 user: User) -> int:
        client_id = user.token_manager.client_id
        refresh_token = user.token_manager.refresh_token
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        url = self._HOSTNAME + self._OAUTH2_PATH
        data = {
            'grant_type': self._GRANT_TYPE_VALUE,
            'client_id': client_id,
            'refresh_token': refresh_token
        }

        response = requests.post(url=url,
                                 headers=header,
                                 data=data,
                                 timeout=self._REQUEST_TIMEOUT)

        response.raise_for_status()

        response_data = response.json()
        user.token_manager.access_token = response_data[self._ACCESS_TOKEN_KEY]
        user.token_manager.refresh_token = response_data[self._REFRESH_TOKEN_KEY]
        logger.warning('Set new access and refresh tokens for user: {}'.format(user.user_id))

        return response.status_code

    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.ConnectionError,
                           requests.exceptions.Timeout),
                          logger=logger,
                          max_tries=_REQUEST_RETRIES
                          )
    def _request(self,
                 user: User,
                 path: str) -> dict:
        access_token = user.token_manager.access_token
        header = {'Authorization': 'Bearer {}'.format(access_token)}
        url = self._HOSTNAME + path

        try:
            response = requests.get(url=url,
                                    headers=header,
                                    timeout=self._REQUEST_TIMEOUT)

            response.raise_for_status()
            return response.json()

        # When the authentication tokens expire and result in HTTPError(401),
        # we need to explicitly handle the token refresh and retry the same request
        except requests.exceptions.HTTPError as ex:
            if ex.response.status_code == 401:
                logger.warning('Encountered authorization error for user: {}'.format(user.user_id))
                status_code = self._refresh()
                logger.debug('Refresh status code: {}'.format(status_code))
                return self._request(path=path)

            else:
                raise ex

    def get_profile(self,
                    user: User) -> dict:
        profile_path = self._PROFILE_PATH.format(str(self._DEFAULT_API_VERSION),
                                                 user.user_id)
        profile = self._request(user=user, path=profile_path)
        return profile
