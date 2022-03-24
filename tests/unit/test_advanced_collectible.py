from brownie import network, AdvancedCollectible
import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVS, get_account, get_contract
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
import time


def test_can_create_advanced_collectible():
    # ? deploy the contract
    # ? create NFT
    # ? get a random breed back as return

    # * arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVS:
        pytest.skip("Only for local testing...")

    # * act
    advanced_collectible, create_transaction = deploy_and_create()
    time.sleep(60)
    requestId = create_transaction.events["requestedCollectible"]["requestId"]
    RANDOM_NUMBER = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, RANDOM_NUMBER, advanced_collectible.address, {"from": get_account()}
    )
    time.sleep(60)

    # * assert
    assert advanced_collectible.tokenCounter() > 0
    assert advanced_collectible.tokenIdToBreed(0) == RANDOM_NUMBER % 3
