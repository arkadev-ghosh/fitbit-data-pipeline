from dotenv import find_dotenv

from fitbit.client import Client
from fitbit.tokens.managers import DotEnvTokenManager
from fitbit.user import User


def main():
    dotenv_path = find_dotenv()
    print("Dot env path: ", dotenv_path)
    token_manager = DotEnvTokenManager(dotenv_path=dotenv_path)
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
