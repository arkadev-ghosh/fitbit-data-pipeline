from api.fitbit.client import Client
from api.fitbit.tokens import DotEnvTokenManager


def main():
    token_manager = DotEnvTokenManager('../.env')
    client = Client(token_manager=token_manager)
    profile = client.get_profile()
    print(profile)


if __name__ == '__main__':
    main()
