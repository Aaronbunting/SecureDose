import streamlit as st
from web3 import Web3
import json
from datetime import datetime

# ...



# Title
st.title("Drug Authenticity Management")

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Sidebar for contract address and private key
contract_address = st.sidebar.text_input("Contract Address", "")
private_key = st.sidebar.text_area("Private Key", "")

if contract_address and private_key:

    # Load ABI
    with open("contract_abi.json", "r") as f:
        contract_abi = json.load(f)

    # Set up contract
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    sender_address = w3.eth.account.from_key(private_key).address
    st.sidebar.write(f"Connected as {sender_address}")

    # Header
    st.header("Choose a Function")
    option = st.selectbox('', ('verifyCompany', 'revokeVerification', 'registerDrug', 'transferDrug', 'fetchTotalDrugs', 'fetchDrugDetails'))

    def send_transaction(tx):
        signed_tx = w3.eth.account.signTransaction(tx, private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        st.write(f"Transaction Hash: {tx_hash.hex()}")

    if option == 'verifyCompany':
        st.subheader("Verify a Company")
        company_address = st.text_input("Company Address to Verify")
        if st.button("Verify Company"):
            tx = contract.functions.verifyCompany(company_address).buildTransaction({
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
            tx = contract.functions.registerDrug(name, components, int(manufacture_timestamp), int(expiry_timestamp), description, token_uri).buildTransaction({
                'gas': 2000000,
                'gasPrice': w3.toWei('40', 'gwei'),
                'nonce': w3.eth.getTransactionCount(sender_address),
            })
            signed_tx = w3.eth.account.signTransaction(tx, private_key)
            tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            st.write(f"Transaction Hash: {tx_hash.hex()}")
        
        

    elif option == 'fetchTotalDrugs':
        if st.button("Fetch Total Drugs"):
            total_drugs = contract.functions.totalDrugs().call()
            st.write(f"Total drugs registered: {total_drugs}")

    elif option == 'fetchDrugDetails':
        drug_id = st.number_input("Enter Drug ID to fetch details", min_value=1, value=1, step=1)
        if st.button("Fetch Drug Details"):
            drug_details = contract.functions.drugs(drug_id).call()
            st.write(f"Drug Details: {drug_details}")

else:
    st.sidebar.write("Please enter the contract address and private key to proceed.")




