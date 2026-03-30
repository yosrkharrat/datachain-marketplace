// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/Ownable.sol";

contract DatasetRegistry is Ownable {
    struct Dataset {
        uint256 id;
        string ipfsHash;
        string title;
        string description;
        uint256 priceWei;
        address owner;
    }

    uint256 private datasetCount;
    Dataset[] private datasets;

    event DatasetRegistered(
        uint256 indexed id,
        address indexed owner,
        string ipfsHash,
        string title,
        uint256 priceWei
    );

    constructor() Ownable(msg.sender) {}

    function registerDataset(
        string calldata ipfsHash,
        string calldata title,
        string calldata description,
        uint256 priceWei
    ) external returns (uint256) {
        require(bytes(ipfsHash).length > 0, "IPFS hash required");
        require(bytes(title).length > 0, "Title required");

        datasetCount += 1;

        Dataset memory dataset = Dataset({
            id: datasetCount,
            ipfsHash: ipfsHash,
            title: title,
            description: description,
            priceWei: priceWei,
            owner: msg.sender
        });

        datasets.push(dataset);

        emit DatasetRegistered(dataset.id, msg.sender, ipfsHash, title, priceWei);

        return dataset.id;
    }

    function getDataset(uint256 id) external view returns (Dataset memory) {
        require(id > 0 && id <= datasetCount, "Dataset does not exist");
        return datasets[id - 1];
    }

    function getAllDatasets() external view returns (Dataset[] memory) {
        return datasets;
    }

    function totalDatasets() external view returns (uint256) {
        return datasetCount;
    }
}
