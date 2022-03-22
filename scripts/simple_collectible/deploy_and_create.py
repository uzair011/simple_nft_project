from scripts.helpful_scripts import get_account, OPENSEA_URL
from brownie import SimpleCollectible, accounts, network, config

sampleCollectibleURI = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"


def deploy_and_create():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
    tracsaction = simple_collectible.createCollectible(
        sampleCollectibleURI, {"from": account}
    )
    tracsaction.wait(1)
    print(
        f"Congratulations, You can view your NFT at {OPENSEA_URL.format(simple_collectible.address, simple_collectible.tokenCounter() - 1)}"
    )
    return simple_collectible


def main():
    deploy_and_create()
