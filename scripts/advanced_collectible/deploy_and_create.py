from web3 import Web3
from scripts.helpful_scripts import (
    get_account,
    OPENSEA_URL,
    get_contract,
    fund_with_link,
)
from brownie import AdvancedCollectible, network, config


def deploy_and_create():
    account = get_account()
    # advanced_collectible = AdvancedCollectible.deploy({"from": account})
    # ? we want to use the deployed contracts if we are on testnet, otherwise, we want to deploy mocks and use those RINKEBY
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
    )
    fund_with_link(advanced_collectible.address)
    creating_transaction = advanced_collectible.createCollectible({"from": account})
    creating_transaction.wait(1)
    print("New token has been created")
    return advanced_collectible, creating_transaction


def main():
    deploy_and_create()
