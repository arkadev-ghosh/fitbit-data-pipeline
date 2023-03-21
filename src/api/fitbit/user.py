from api.fitbit.token import TokenManager


class User:
    _DEFAULT_USER_ID: str = '-'

    def __init__(self,
                 token_manager: TokenManager,
                 user_id: str = _DEFAULT_USER_ID):
        self.token_manager = token_manager
        self.user_id = user_id
        self._profile = None

    @property
    def profile(self):
        return self._profile

    @profile.setter
    def profile(self,
                value):
        self._profile = value
