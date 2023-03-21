import backoff
import requests

from api.fitbit.token import TokenManager


class Client:
    _HOSTNAME: str = 'https://api.fitbit.com'
    _API_VERSION: str = '1'
    _OAUTH2_PATH: str = '/oauth2/token'
    _DEFAULT_USER_ID: str = '-'
    _API_TIMEOUT: float = 5.0

    def __init__(self,
                 token_manager: TokenManager,
                 user_id: str = _DEFAULT_USER_ID) -> None:
        self._token_manager = token_manager
        self._user_id = user_id

    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.ConnectionError,
                           requests.exceptions.Timeout)
                          )
    def _refresh(self) -> int:
        client_id = self._token_manager.client_id
        refresh_token = self._token_manager.refresh_token
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        url = self._HOSTNAME + self._OAUTH2_PATH
        data = {
            'grant_type': 'refresh_token',
            'client_id': client_id,
            'refresh_token': refresh_token
        }

        response = requests.post(url=url,
                                 headers=header,
                                 data=data,
                                 timeout=self._API_TIMEOUT)

        response.raise_for_status()

        response_data = response.json()
        self._token_manager.access_token = response_data['access_token']
        self._token_manager.refresh_token = response_data['refresh_token']

        return response.status_code

    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.ConnectionError,
                           requests.exceptions.Timeout)
                          )
    def _request(self,
                 path: str) -> dict:
        access_token = self._token_manager.access_token
        header = {'Authorization': 'Bearer {}'.format(access_token)}
        url = self._HOSTNAME + path

        try:
            response = requests.get(url=url,
                                    headers=header,
                                    timeout=self._API_TIMEOUT)

            response.raise_for_status()
            return response.json()

        # When the authentication tokens expire and result in HTTPError(401),
        # we need to explicitly handle the token refresh and retry the same request
        except requests.exceptions.HTTPError as ex:
            if ex.response.status_code == 401:
                print(str(ex))
                self._refresh()
                return self._request(path=path)

            else:
                raise ex

    @property
    def profile(self) -> dict:
        profile_path = '/{}/user/{}/profile.json'.format(self._API_VERSION,
                                                         self._user_id)
        profile = self._request(path=profile_path)
        return profile
