from api.fitbit.client import Client
from api.fitbit.tokens import DotEnvTokenManager
from api.fitbit.user import User


def main():
    token_manager = DotEnvTokenManager('../.env')
    fitbit_user = User(token_manager=token_manager)
    fitbit_client = Client()

    fitbit_user.profile = fitbit_client.get_profile(fitbit_user)
    print(fitbit_user.profile)


if __name__ == '__main__':
    main()
