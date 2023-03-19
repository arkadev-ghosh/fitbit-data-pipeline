import dotenv
from dotenv import dotenv_values
from dotenv import load_dotenv

from api.fitbit.token import TokenManager


class DotEnvTokenManager(TokenManager):
    def __init__(self,
                 dotenv_path: str) -> None:
        load_dotenv(dotenv_path=dotenv_path)
        self.dotenv_path = dotenv_path

    @property
    def access_token(self) -> str:
        return dotenv_values(dotenv_path=self.dotenv_path)[self._ACCESS_TOKEN_KEY]

    @access_token.setter
    def access_token(self,
                     value: str) -> None:
        dotenv.set_key(dotenv_path=self.dotenv_path,
                       key_to_set=self._ACCESS_TOKEN_KEY,
                       value_to_set=value)

    @property
    def refresh_token(self) -> str:
        return dotenv_values(dotenv_path=self.dotenv_path)[self._REFRESH_TOKEN_KEY]

    @refresh_token.setter
    def refresh_token(self,
                      value: str) -> None:
        dotenv.set_key(dotenv_path=self.dotenv_path,
                       key_to_set=self._REFRESH_TOKEN_KEY,
                       value_to_set=value)
