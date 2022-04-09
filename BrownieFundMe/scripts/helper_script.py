from brownie import MockV3Aggregator, accounts, network, config
from web3 import Web3
import sys

DECIMALS = 18
STARTING_PRICE = Web3.toWei(2000, "ether")


def get_account():
    if network.show_active() == "development" or sys.argv[-1] == "ganache-local":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"Active Network: {network.show_active()}")
    print("Deploying Mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
    print("Mocks Deployed!")
