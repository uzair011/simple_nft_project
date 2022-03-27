from pickle import TRUE
from scripts.helpful_scripts import get_breed
from brownie import AdvancedCollectible, network
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests, json, os

breedToImageUri = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_collectibles} collectibles")
    for token_id in range(number_of_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists. Delete it to override..")
        else:
            print(f"Creating metadata file : {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"A beautiful {breed} pug!"
            print(collectible_metadata)
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"
            imate_uri = None
            if os.getenv("UPLOAD_IPFS") == TRUE:
                image_uri = upload_to_ipfs(image_path)
            image_uri = image_uri if image_uri else breedToImageUri[breed]

            collectible_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == True:
                upload_to_ipfs(metadata_file_name)


def upload_to_ipfs(filePath):
    with Path(filePath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        end_point = "/api/v0/add"
        response = requests.post(ipfs_url + end_point, files={"file": image_binary})
        ipfs_hash = response.json()["hash"]
        # ./img/0-pug.png ===> 0-pug.png  (remove all the "/" and get the img name with the extension )
        file_name = filePath.split("/")[-1:][0]
        img_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={file_name}"
        print(img_uri)
        return img_uri
