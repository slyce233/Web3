from brownie import accounts, config, SimpleStorage, network


def deploy_simple_storage():
    account = get_account()
    from_address = {"from": account}

    simple_storage = SimpleStorage.deploy(from_address)
    stored_value = simple_storage.retrieve()

    print(stored_value)

    transaction = simple_storage.store(15, (from_address))
    transaction.wait(1)

    updated_stored_value = simple_storage.retrieve()

    print(updated_stored_value)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()
