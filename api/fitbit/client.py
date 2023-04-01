import logging

import backoff
import requests

from .user import User

logger = logging.getLogger(__name__)


class Client:
    # WebAPI endpoint details
    _HOSTNAME: str = 'https://api.fitbit.com'
    _OAUTH2_PATH: str = '/oauth2/token'
    _USER_PATH: str = '/{}/user/{}/profile.json'
    _SLEEP_BY_RANGE_PATH: str = '/{}/user/{}/sleep/date/{}/{}.json'
    _SLEEP_BY_DATE_PATH: str = '/{}/user/{}/sleep/date/{}.json'

    # WebAPI endpoint version details
    _DEFAULT_USER_API_VERSION: str = '1'
    _DEFAULT_SLEEP_API_VERSION: str = '1.2'

    # HTTP request timeout, retries
    _REQUEST_TIMEOUT: float = 10.0
    _REQUEST_RETRIES: int = 5

    # Request, Response data key/values
    _GRANT_TYPE_VALUE: str = 'refresh_token'
    _ACCESS_TOKEN_KEY: str = 'access_token'
    _REFRESH_TOKEN_KEY: str = 'refresh_token'

    def __init__(self,
                 user_api_version: str = _DEFAULT_USER_API_VERSION,
                 sleep_api_version: str = _DEFAULT_SLEEP_API_VERSION) -> None:
        self._user_api_version = user_api_version
        self._sleep_api_version = sleep_api_version

    @classmethod
    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.ConnectionError,
                           requests.exceptions.Timeout),
                          logger=logger,
                          max_tries=_REQUEST_RETRIES
                          )
    def _refresh(cls,
                 user: User) -> int:
        client_id = user.token_manager.client_id
        refresh_token = user.token_manager.refresh_token
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        url = cls._HOSTNAME + cls._OAUTH2_PATH
        data = {
            'grant_type': cls._GRANT_TYPE_VALUE,
            'client_id': client_id,
            'refresh_token': refresh_token
        }

        response = requests.post(url=url,
                                 headers=header,
                                 data=data,
                                 timeout=cls._REQUEST_TIMEOUT)

        response.raise_for_status()

        response_data = response.json()
        user.token_manager.access_token = response_data[cls._ACCESS_TOKEN_KEY]
        user.token_manager.refresh_token = response_data[cls._REFRESH_TOKEN_KEY]
        logger.warning('Set new access and refresh tokens for user: %s', user.user_id)

        return response.status_code

    @classmethod
    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.ConnectionError,
                           requests.exceptions.Timeout),
                          logger=logger,
                          max_tries=_REQUEST_RETRIES
                          )
    def _request(cls,
                 user: User,
                 path: str) -> dict:
        access_token = user.token_manager.access_token
        header = {'Authorization': f'Bearer {access_token}'}
        url = Client._HOSTNAME + path

        try:
            response = requests.get(url=url,
                                    headers=header,
                                    timeout=Client._REQUEST_TIMEOUT)

            response.raise_for_status()
            return response.json()

        # When the authentication tokens expire and result in HTTPError(401),
        # we need to explicitly handle the tokens refresh and retry the same request
        except requests.exceptions.HTTPError as ex:
            if ex.response.status_code == 401:
                logger.warning('Encountered authorization error for user: %s', user.user_id)
                status_code = cls._refresh(user=user)
                logger.debug('Refresh status code: %s', status_code)
                return cls._request(user=user,
                                    path=path)

            raise ex

    def get_profile(self,
                    user: User) -> dict:
        profile_path = self._USER_PATH.format(self._user_api_version,
                                              user.user_id)
        profile = self._request(user=user,
                                path=profile_path)
        return profile

    def get_sleep_log(self,
                      user: User,
                      start_date: str,
                      end_date: str = None) -> dict:
        if end_date:
            sleep_log_path = self._SLEEP_BY_RANGE_PATH.format(self._sleep_api_version,
                                                              user.user_id,
                                                              start_date,
                                                              end_date)

        else:
            sleep_log_path = self._SLEEP_BY_DATE_PATH.format(self._sleep_api_version,
                                                             user.user_id,
                                                             start_date)

        sleep_log = self._request(user=user,
                                  path=sleep_log_path)

        return sleep_log
