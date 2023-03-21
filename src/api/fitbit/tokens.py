import dotenv
from dotenv import dotenv_values

from api.fitbit.token import TokenManager


class DotEnvTokenManager(TokenManager):
    def __init__(self,
                 dotenv_path: str) -> None:
        self.dotenv_path = dotenv_path
        self._client_id = dotenv_values(dotenv_path=self.dotenv_path)[self._CLIENT_ID_KEY]
        self._access_token = dotenv_values(dotenv_path=self.dotenv_path)[self._ACCESS_TOKEN_KEY]
        self._refresh_token = dotenv_values(dotenv_path=self.dotenv_path)[self._REFRESH_TOKEN_KEY]

    @property
    def client_id(self) -> str:
        return self._client_id

    @client_id.setter
    def client_id(self,
                  value) -> None:
        dotenv.set_key(dotenv_path=self.dotenv_path,
                       key_to_set=self._CLIENT_ID_KEY,
                       value_to_set=value)

        self._client_id = dotenv_values(dotenv_path=self.dotenv_path)[self._CLIENT_ID_KEY]

    @property
    def access_token(self) -> str:
        return self._access_token

    @access_token.setter
    def access_token(self,
                     value: str) -> None:
        dotenv.set_key(dotenv_path=self.dotenv_path,
                       key_to_set=self._ACCESS_TOKEN_KEY,
                       value_to_set=value)

        self._access_token = dotenv_values(dotenv_path=self.dotenv_path)[self._ACCESS_TOKEN_KEY]

    @property
    def refresh_token(self) -> str:
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self,
                      value: str) -> None:
        dotenv.set_key(dotenv_path=self.dotenv_path,
                       key_to_set=self._REFRESH_TOKEN_KEY,
                       value_to_set=value)

        self._refresh_token = dotenv_values(dotenv_path=self.dotenv_path)[self._REFRESH_TOKEN_KEY]
