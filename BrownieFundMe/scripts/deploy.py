from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helper_script import get_account, deploy_mocks
from web3 import Web3
import sys


def deploy_fund_me():
    account = get_account()

    # check for network and deploy address or mock
    if network.show_active() == "development" or sys.argv[-1] == "ganache-local":
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
    else:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")


def main():
    deploy_fund_me()
