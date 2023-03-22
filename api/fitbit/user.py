from .tokens.manager import TokenManager


class User:
    _DEFAULT_USER_ID: str = '-'

    def __init__(self,
                 token_manager: TokenManager,
                 user_id: str = _DEFAULT_USER_ID):
        self._token_manager = token_manager
        self._user_id = user_id
        self._profile = None

    @property
    def token_manager(self):
        return self._token_manager

    @property
    def user_id(self):
        return self._user_id

    @property
    def profile(self):
        return self._profile

    @profile.setter
    def profile(self,
                value):
        self._profile = value
