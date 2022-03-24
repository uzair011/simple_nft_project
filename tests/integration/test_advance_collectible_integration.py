from brownie import network, AdvancedCollectible
import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVS, get_account, get_contract
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
import time


def test_can_create_advanced_collectible_integration():
    # ? deploy the contract
    # ? create NFT
    # ? get a random breed back as return

    # * arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVS:
        pytest.skip("Only for integration testing...")

    # * act
    advanced_collectible, create_transaction = deploy_and_create()
    time.sleep(60)

    # * assert
    assert advanced_collectible.tokenCounter() == 1
