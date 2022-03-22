from brownie import (
    accounts,
    network,
    config,
    VRFCoordinatorMock,
    linkToken,
    Contract,
    MockV3Aggregator,
)


OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
LOCAL_BLOCKCHAIN_ENVS = ["development", "ganache-local", "mainnet-fork-dev"]


def get_account(id=None, index=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVS:
        return accounts[0]
    if network.show_active() in config["networks"]:
        return accounts.add(config["wallets"]["from_key"])
    return None


contract_to_mock = {
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": linkToken,
    # "key_hash": keyhash,
}


def get_contract(contract_name):
    """
    this function will grab the contract addresses from the brownie config if defined, otherwise, it will
    deploy a MOCK version of that contract, and return that contract.

    Args:
        contract_name ( string )
    returns:
        Brownie.network.contract.projectContract: The most recently deployed version of this contract.
        --> MockV3Aggregator[-1]

    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]

        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.address
        )
    return contract


DECIMALS = 8
INITIAL_VALUE = 200000000000


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = linkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("D E P L O Y E D . . . ! ! !")
