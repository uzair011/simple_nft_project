from scripts.helpful_scripts import get_account, OPENSEA_URL
from brownie import AdvancedCollectible, accounts, network, config


def deploy_and_create():
    account = get_account()
    advanced_collectible = AdvancedCollectible.deploy({"from": account})


def main():
    deploy_and_create()
