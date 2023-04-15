import logging

import backoff
import dotenv
from botocore import exceptions
from dotenv import dotenv_values

from extractors.fitbit.conn.tokens.manager import TokenManager

logger = logging.getLogger(__name__)


class DotEnvTokenManager(TokenManager):
    def __init__(self,
                 dotenv_path: str) -> None:
        self._dotenv_path = dotenv_path
        self._client_id = dotenv_values(dotenv_path=self._dotenv_path)[TokenManager._CLIENT_ID_KEY]
        self._access_token = dotenv_values(dotenv_path=self._dotenv_path)[TokenManager._ACCESS_TOKEN_KEY]
        self._refresh_token = dotenv_values(dotenv_path=self._dotenv_path)[TokenManager._REFRESH_TOKEN_KEY]

    @property
    def client_id(self) -> str:
        return self._client_id

    @client_id.setter
    def client_id(self,
                  value) -> None:
        dotenv.set_key(dotenv_path=self._dotenv_path,
                       key_to_set=TokenManager._CLIENT_ID_KEY,
                       value_to_set=value)

        self._client_id = value

    @property
    def access_token(self) -> str:
        return self._access_token

    @access_token.setter
    def access_token(self,
                     value: str) -> None:
        dotenv.set_key(dotenv_path=self._dotenv_path,
                       key_to_set=TokenManager._ACCESS_TOKEN_KEY,
                       value_to_set=value)

        self._access_token = value

    @property
    def refresh_token(self) -> str:
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self,
                      value: str) -> None:
        dotenv.set_key(dotenv_path=self._dotenv_path,
                       key_to_set=TokenManager._REFRESH_TOKEN_KEY,
                       value_to_set=value)

        self._refresh_token = value


class SSMTokenManager(TokenManager):
    _PARAMETER_KEY = 'Parameter'
    _VALUE_KEY = 'Value'
    _REQUEST_RETRIES = 3

    def __init__(self,
                 ssm_client):
        self._ssm_client = ssm_client
        self._client_id = self._get_parameter(name=TokenManager._CLIENT_ID_KEY)
        self._access_token = self._get_parameter(name=TokenManager._ACCESS_TOKEN_KEY)
        self._refresh_token = self._get_parameter(name=TokenManager._REFRESH_TOKEN_KEY)

    @backoff.on_exception(backoff.expo,
                          (exceptions.ClientError,),
                          logger=logger,
                          max_tries=_REQUEST_RETRIES)
    def _get_parameter(self,
                       name,
                       with_decryption=True):
        return (
            self._ssm_client.get_parameter(Name=name, WithDecryption=with_decryption)
            [SSMTokenManager._PARAMETER_KEY][SSMTokenManager._VALUE_KEY]
        )

    @backoff.on_exception(backoff.expo,
                          (exceptions.ClientError,),
                          logger=logger,
                          max_tries=_REQUEST_RETRIES)
    def _put_parameter(self,
                       name,
                       value,
                       ptype,
                       overwrite,
                       tier):
        self._ssm_client.put_parameter(Name=name,
                                       Value=value,
                                       Type=ptype,
                                       Overwrite=overwrite,
                                       Tier=tier)

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self,
                  value) -> None:
        self._put_parameter(name=TokenManager._CLIENT_ID_KEY,
                            value=value,
                            ptype='String',
                            overwrite=True,
                            tier='Standard')

        self._client_id = value

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self,
                     value: str) -> None:
        self._put_parameter(name=TokenManager._ACCESS_TOKEN_KEY,
                            value=value,
                            ptype='SecureString',
                            overwrite=True,
                            tier='Standard')

        self._access_token = value

    @property
    def refresh_token(self):
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self,
                      value: str) -> None:
        self._put_parameter(name=TokenManager._REFRESH_TOKEN_KEY,
                            value=value,
                            ptype='SecureString',
                            overwrite=True,
                            tier='Standard')

        self._refresh_token = value
