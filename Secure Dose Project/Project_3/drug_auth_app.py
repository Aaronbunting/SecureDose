import streamlit as st
from web3 import Web3
import json
from datetime import datetime

# Title
st.title("Drug Authenticity Management")

# Connect to Ethereum Network
w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/49730444bc104b2680a006a41689b892'))

# Sidebar for contract address and private key
contract_address = st.sidebar.text_input("Contract Address", "0x2139ee923189139fA0E1695f3E0d6f694Ed3BC0e")
private_key = st.sidebar.text_area("Private Key", "72c2044edb1cee5a80b5a5b25f5c08ecd5d2d567db1bce8fbb5ea8a7f534c200")

def send_transaction(tx):
    
    try:
        signed_tx = w3.eth.account.signTransaction(tx, private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        st.write(f"Transaction Hash: {tx_hash.hex()}")
    except Exception as e:
        st.error(f"Error sending transaction: {e}")

elif contract_address and private_key:

    # Validate Private Key
    if len(private_key) != 64:
        st.sidebar.error("Invalid private key!")
        raise st.ScriptRunner.StopException

    # Load ABI
    with open("contract_abi.json", "r") as f:
        contract_abi = json.load(f)

    # Set up contract
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    sender_address = w3.eth.account.privateKeyToAccount(private_key).address
    st.sidebar.write(f"Connected as {sender_address}")

    # Header
    st.header("Choose a Function")
    option = st.selectbox('', ('verifyCompany', 'revokeVerification', 'registerDrug', 'transferDrug', 'fetchTotalDrugs', 'fetchDrugDetails', 'drugsByCompanyAddress', 'getAllVerifiedCompanies'))

    if option == 'verifyCompany':
        st.subheader("Verify a Company")
        company_address = st.text_input("Company Address to Verify")
        company_name = st.text_input("Company Name")
        if st.button("Verify Company"):
            tx = contract.functions.verifyCompany(company_address, company_name).buildTransaction({
                'gas': 2000000,
                'gasPrice': w3.toWei('40', 'gwei'),
                'nonce': w3.eth.getTransactionCount(sender_address),
            })
            send_transaction(tx)

    elif option == 'revokeVerification':
        st.subheader("Revoke Verification of a Company")
        company_address = st.text_input("Company Address to Revoke")
        if st.button("Revoke Verification"):
            tx = contract.functions.revokeVerification(company_address).buildTransaction({
                'gas': 2000000,
                'gasPrice': w3.toWei('40', 'gwei'),
                'nonce': w3.eth.getTransactionCount(sender_address),
            })
            send_transaction(tx)

    elif option == 'registerDrug':
        st.subheader("Register a Drug")
        name = st.text_input("Drug Name")
        components = st.text_input("Components (comma-separated)")
        manufacture_date = st.date_input("Manufacture Date")
        expiry_date = st.date_input("Expiry Date")
        description = st.text_area("Description")
        token_uri = st.text_input("Token URI")
        
        manufacture_timestamp = datetime.combine(manufacture_date, datetime.min.time()).timestamp()
        expiry_timestamp = datetime.combine(expiry_date, datetime.min.time()).timestamp()

        if st.button("Register Drug"):
            st.write("Processing... Please wait.")
            try:
                estimated_gas = contract.functions.registerDrug(name, components, int(manufacture_timestamp), int(expiry_timestamp), description, token_uri).estimateGas()
                tx = contract.functions.registerDrug(name, components, int(manufacture_timestamp), int(expiry_timestamp), description, token_uri).buildTransaction({
                    'gas': 2000000,
                    'gasPrice': w3.toWei('40', 'gwei'),
                    'nonce': w3.eth.getTransactionCount(sender_address),
                })
                send_transaction(tx)
            except Exception as e:
                st.error(f"An error occurred: {e}")

    elif option == 'transferDrug':
        st.subheader("Transfer Drug")
        recipient_address = st.text_input("Recipient Address")
        drug_id = st.number_input("Drug ID", min_value=0)
        if st.button("Transfer Drug"):
            tx = contract.functions.transferDrug(recipient_address, drug_id).buildTransaction({
                'gas': 2000000,
                'gasPrice': w3.toWei('40', 'gwei'),
                'nonce': w3.eth.getTransactionCount(sender_address),
            })
            send_transaction(tx)

    elif option == 'fetchTotalDrugs':
        if st.button("Fetch Total Drugs"):
            total_drugs = contract.functions.totalDrugs().call()
            st.write(f"Total drugs registered: {total_drugs}")

    elif option == 'fetchDrugDetails':
        drug_id = st.number_input("Enter Drug ID to fetch details", min_value=1, value=1, step=1)
        if st.button("Fetch Drug Details"):
            drug_details = contract.functions.drugs(drug_id).call()
            st.write(f"Drug Details: {drug_details}")

    elif option == 'drugsByCompanyAddress':
        company_address = st.text_input("Enter Company Address to fetch all registered drugs")
        if st.button("Fetch Drugs By Company"):
            drugs = contract.functions.drugsByCompanyAddress(company_address).call()
            st.write(f"Drugs registered by the company: {drugs}")

    elif option == 'getAllVerifiedCompanies':
        if st.button("Fetch All Verified Companies"):
            verified_companies = contract.functions.getAllVerifiedCompanies().call()
            st.write(f"Verified Companies: {verified_companies}")

else:
    st.sidebar.write("Please enter the contract address and private key to proceed.")


