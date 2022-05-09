from brownie import MockV3Aggregator, accounts, network, config
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork-dev", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONENTS = ["development", "ganache-local"]
DECIMALS = 18
STARTING_PRICE = 2000000000000


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"Active Network: {network.show_active()}")
    print("Deploying Mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
    print("Mocks Deployed!")
