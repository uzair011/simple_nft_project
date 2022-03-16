from scripts.helpful_scripts import get_account


from scripts.helpful_scripts import get_account, SimpleCollectible


def main():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"form": account})
