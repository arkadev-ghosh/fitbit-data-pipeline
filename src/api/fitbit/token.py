from abc import abstractmethod
from typing import Protocol


class TokenManager(Protocol):
    _ACCESS_TOKEN_KEY: str = 'ACCESS_TOKEN'
    _REFRESH_TOKEN_KEY: str = 'REFRESH_TOKEN'

    @property
    @abstractmethod
    def access_token(self):
        raise NotImplementedError

    @access_token.setter
    @abstractmethod
    def access_token(self,
                     value):
        raise NotImplementedError

    @property
    @abstractmethod
    def refresh_token(self):
        raise NotImplementedError

    @refresh_token.setter
    @abstractmethod
    def refresh_token(self,
                      value):
        raise NotImplementedError
