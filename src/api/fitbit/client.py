import requests

from api.fitbit.token import TokenManager


class Client:
    _FITBIT_API_ENDPOINT: str = 'https://api.fitbit.com/1'
    _FITBIT_DEFAULT_USER_ID: str = '-'

    def _request(self,
                 endpoint_suffix: str) -> dict:
        access_token = self._token_manager.access_token
        header = {'Authorization': 'Bearer {}'.format(access_token)}
        url = self._FITBIT_API_ENDPOINT + endpoint_suffix
        response = requests.get(url=url,
                                headers=header)
        response.raise_for_status()
        return response.json()

    def __init__(self,
                 token_manager: TokenManager,
                 user_id: str = _FITBIT_DEFAULT_USER_ID) -> None:
        self._token_manager = token_manager
        self._user_id = user_id

    def get_profile(self) -> dict:
        profile_endpoint_suffix = f'/user/{self._user_id}/profile.json'
        profile = self._request(endpoint_suffix=profile_endpoint_suffix)
        return profile
