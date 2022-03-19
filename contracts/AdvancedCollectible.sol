// This is an NFT contract, the tokenURI can be one of the 3 NFT's
//and it will get selected randomly.

// SPDX-License-Identifier: MIT

pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;
    enum Breed {
        PUG,
        SHIBA_INU,
        ST_BERNERD
    }
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(bytes32 => address) public requestIdToSender;
    event requestedCollectible(bytes32 indexed requestId, address requester);
    event breedAssigned(uint256 indexed tokenId, Breed breed);

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyhash,
        uint256 _fee
    )
        public
        VRFConsumerBase(_vrfCoordinator, _linkToken)
        ERC721("happyDog", "DOG")
    {
        tokenCounter = 0;
        keyhash = _keyhash;
        fee = _fee;
    }

    function createCollectible(string memory tokenURI)
        public
        returns (bytes32)
    {
        bytes32 requestId = requestRandomness(keyhash, fee);
        requestIdToSenter[requestId] = msg.sender;
        //requestidToTokenURI[requestId] = tokenURI; //////// here...
        emit requestedCollectible(requestId, msg.sender);
    }

    function fullFillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        Breed breed = Breed(randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToBreed[newTokenId] = breed;
        emit breedAssigned(newTokenId, breed);
        address owner = requestIdToSender[requestId];
        _safeMInt(owner, newTokenId);
        //_setTokenURI(newTokenId, tokenURI);
        tokenCounter += tokenCounter;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        // pug shiba-inu, st-bernard
        require(
            _isApprovedOrOwner(
                _msgSender(),
                tokenId,
                "ERC721: caller isn't owner approved..."
            )
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}