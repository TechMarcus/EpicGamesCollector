from games_collector import EgsAccount
import asyncio


def main():
    test_user = EgsAccount(user="range")
    test_user.collector()

if __name__ == "__main__":
    main()