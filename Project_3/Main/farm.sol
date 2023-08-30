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
    
    struct Company {
        string name;
        bool isVerified;
    }

    uint256[] public DrugIDs; // Made this public for easy access
    mapping(uint256 => Drug) public drugs;
    mapping(address => uint256[]) public drugsByCompany;
    mapping(address => Company) public companies;
    address[] public verifiedCompanyAddresses;

    modifier onlyVerifiedCompany() {
        require(companies[msg.sender].isVerified, "Not a verified pharmaceutical company");
        _;
    }

    constructor() public ERC721Full("DrugAuthenticity", "DAUTH") {}

    function verifyCompany(address company, string memory name) public onlyOwner {
        companies[company].name = name;
        if(!companies[company].isVerified) {
            companies[company].isVerified = true;
            verifiedCompanyAddresses.push(company);
        }
    }

    function revokeVerification(address company) public onlyOwner {
        companies[company].isVerified = false;
    }

    event DrugRegistered(uint256 drugId, address registeredBy);

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
        drugsByCompany[msg.sender].push(newDrugId);
        _mint(msg.sender, newDrugId);
        _setTokenURI(newDrugId, tokenURI);

        DrugIDs.push(newDrugId);
        emit DrugRegistered(newDrugId, msg.sender);  // Emitting the event
        return newDrugId;
    }

    function transferDrug(address to, uint256 drugId) public {
        require(ownerOf(drugId) == msg.sender, "Only the owner can transfer");
        _transferFrom(msg.sender, to, drugId);
    }

    function totalDrugs() public view returns (uint256) {
        return DrugIDs.length;
    }

    function drugsByCompanyAddress(address companyAddress) public view returns (uint256[] memory) {
        return drugsByCompany[companyAddress];
    }

    function getAllVerifiedCompanies() public view returns (address[] memory) {
        return verifiedCompanyAddresses;
    }
}
