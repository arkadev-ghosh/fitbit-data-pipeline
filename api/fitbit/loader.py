import boto3

from conn.client import Client
from conn.tokens.managers import SSMTokenManager
from conn.user import User


def main():
    session = boto3.session.Session()
    ssm_client = session.client(
        service_name='ssm',
        region_name='us-east-1'
    )

    token_manager = SSMTokenManager(ssm_client=ssm_client)
    fitbit_user = User(token_manager=token_manager)
    fitbit_client = Client()

    fitbit_user.profile = fitbit_client.get_profile(fitbit_user)
    fitbit_user.sleep_log = fitbit_client.get_sleep_log(fitbit_user, start_date='2022-10-12')

    print(fitbit_user.profile)
    data = fitbit_user.sleep_log['sleep']
    for entry in data:
        print(entry)


if __name__ == '__main__':
    main()
