from brownie import config, accounts, network, VRFCoordinatorMock, LinkToken, Contract
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVS = ["development", "ganache-local", "mainnet-fork-dev"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}


def get_breed(breed_number):
    return BREED_MAPPING[breed_number]


def get_account(id=None, index=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {"link_token": LinkToken, "vrf_coordinator": VRFCoordinatorMock}


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
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks():
    print(f"the active network is {network.show_active()}")
    print("Deploying mocks")
    account = get_account()
    print("Deploying mock link token")
    # MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    print(f"Link token deployed to {link_token.address}")
    print("Deploying mock vrfcoordinator")
    vrf_coordinator = VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print(f"VRFcoordinator deploying to {vrf_coordinator.address}")
    print("D E P L O Y E D . . .done ! ! !")


def fund_with_link(
    contract_address, account=None, link_token=None, amount=Web3.toWei(1, "ether")
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    funding_transaction = link_token.transfer(
        contract_address, amount, {"from": account}
    )
    funding_transaction.wait(1)
    print(f"Funded {contract_address}")
    return funding_transaction
