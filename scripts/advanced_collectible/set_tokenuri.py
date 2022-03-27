from lib2to3.pgen2 import token
from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import OPENSEA_URL, get_account, get_breed

DICTIONARY_DOG_METADATA = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}


def main():
    print(f"Working from {network.show_active()}")
    advanced_collectivle = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectivle.tokenCounter()
    print(f"You have {number_of_collectibles} tokenIds")
    for token_id in range(number_of_collectibles):
        breed = get_breed(advanced_collectivle.tokenIdToBreed(token_id))
        if not advanced_collectivle.tokenURI(token_id).startsWith("https://"):
            print(f"Setting token URI of {token_id} ")
            set_tokenURI(token_id, advanced_collectivle, DICTIONARY_DOG_METADATA[breed])


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    transaction = nft_contract.setokenURI(token_id, tokenURI, {"from": account})
    transaction.wait(1)
    print(
        f"Greate, now you can view your nft at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    print("Please wait upto 20 minutes and refresh the metadata.")
