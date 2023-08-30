pragma solidity ^0.5.0;
pragma experimental ABIEncoderV2;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/ownership/Ownable.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/cryptography/ECDSA.sol";

contract DrugAuthenticity is ERC721Full, Ownable {

    using ECDSA for bytes32;

    struct DrugInfo {
        string name;
        string components;
        string description;
        string batchNumber;
        string manufacturingLocation;
        bool isRecalled;
        address registeredBy;
        bytes signature;
    }

    struct DrugDates {
        uint256 manufactureDate;
        uint256 expiryDate;
    }

    mapping(uint256 => DrugInfo) public drugs;
    mapping(uint256 => DrugDates) public drugDates;
    mapping(address => bool) public verifiedCompanies;

    uint256 public maxGasAllowed = 200000;  // Example starting value, adjust as needed

    event CustodyTransfer(address indexed from, address indexed to, uint256 indexed drugId, uint256 date);

    modifier onlyVerifiedCompany() {
        require(verifiedCompanies[msg.sender], "Not a verified pharmaceutical company");
        _;
    }

    constructor() public ERC721Full("DrugAuthenticity", "DAUTH") {}

    function setMaxGasAllowed(uint256 _maxGas) public onlyOwner {
        maxGasAllowed = _maxGas;
    }

    function verifyCompany(address company) public onlyOwner {
        verifiedCompanies[company] = true;
    }

    function revokeVerification(address company) public onlyOwner {
        verifiedCompanies[company] = false;
    }

    function registerDrug(
        DrugInfo memory info,
        DrugDates memory dates,
        string memory tokenURI
    ) 
        public onlyVerifiedCompany 
        returns (uint256) 
    {
        uint256 startingGas = gasleft();  // Capture starting gas

        uint256 newDrugId = totalSupply().add(1);
        
        drugs[newDrugId] = info;
        drugDates[newDrugId] = dates;

        _mint(msg.sender, newDrugId);
        _setTokenURI(newDrugId, tokenURI);

        // Check gas consumption
        require(startingGas - gasleft() <= maxGasAllowed, "Gas consumption exceeds the limit");

        return newDrugId;
    }

    function isExpired(uint256 drugId) public view returns (bool) {
        return drugDates[drugId].expiryDate < now;
    }

    function recallDrug(uint256 drugId) public onlyVerifiedCompany {
        require(msg.sender == drugs[drugId].registeredBy, "Only the registering company can recall this drug");
        drugs[drugId].isRecalled = true;
    }

    function transferDrug(address to, uint256 drugId) public {
        require(ownerOf(drugId) == msg.sender, "Only the owner can transfer");
        _transferFrom(msg.sender, to, drugId);
        emit CustodyTransfer(msg.sender, to, drugId, now);
    }

    function verifySignature(uint256 drugId) public view returns (bool) {
        bytes32 hash = keccak256(abi.encodePacked(
            drugs[drugId].name,
            drugs[drugId].components,
            drugDates[drugId].manufactureDate,
            drugDates[drugId].expiryDate,
            drugs[drugId].description,
            drugs[drugId].batchNumber,
            drugs[drugId].manufacturingLocation
        ));
        
        // The signature should match the registering company's address
        return drugs[drugId].registeredBy == hash.toEthSignedMessageHash().recover(drugs[drugId].signature);
    }
}
