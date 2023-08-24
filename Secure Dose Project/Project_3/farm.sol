pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/ownership/Ownable.sol";

contract DrugAuthenticity is ERC721Full, Ownable {

    struct Drug {
        string name;
        string components;  // For simplicity, components are stored as a comma-separated string
        uint256 manufactureDate;
        uint256 expiryDate;
        string description; // Any additional information
        address registeredBy; // Pharmaceutical company that introduced it
    }

    mapping(uint256 => Drug) public drugs;
    mapping(address => bool) public verifiedCompanies;

    modifier onlyVerifiedCompany() {
        require(verifiedCompanies[msg.sender], "Not a verified pharmaceutical company");
        _;
    }

    constructor() public ERC721Full("DrugAuthenticity", "DAUTH") {}

    // Owner of the contract can approve pharmaceutical companies
    function verifyCompany(address company) public onlyOwner {
        verifiedCompanies[company] = true;
    }

    // Owner of the contract can revoke verification of pharmaceutical companies
    function revokeVerification(address company) public onlyOwner {
        verifiedCompanies[company] = false;
    }

    function registerDrug(
        string memory name,
        string memory components,
        uint256 manufactureDate,
        uint256 expiryDate,
        string memory description,
        string memory tokenURI
    ) 
        public onlyVerifiedCompany 
        returns (uint256) 
    {
        uint256 newDrugId = totalSupply();
        
        Drug memory newDrug = Drug({
            name: name,
            components: components,
            manufactureDate: manufactureDate,
            expiryDate: expiryDate,
            description: description,
            registeredBy: msg.sender
        });

        drugs[newDrugId] = newDrug;
        _mint(msg.sender, newDrugId);
        _setTokenURI(newDrugId, tokenURI);

        return newDrugId;
    }

    // For traceability, transfer is public
    function transferDrug(address to, uint256 drugId) public {
        require(ownerOf(drugId) == msg.sender, "Only the owner can transfer");
        _transferFrom(msg.sender, to, drugId);
    }
}
