from abc import ABC
from abc import abstractmethod


class TokenManager(ABC):
    _CLIENT_ID_KEY = 'CLIENT_ID'
    _ACCESS_TOKEN_KEY: str = 'ACCESS_TOKEN'
    _REFRESH_TOKEN_KEY: str = 'REFRESH_TOKEN'

    @property
    @abstractmethod
    def client_id(self):
        raise NotImplementedError

    @client_id.setter
    @abstractmethod
    def client_id(self,
                  value):
        raise NotImplementedError

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
