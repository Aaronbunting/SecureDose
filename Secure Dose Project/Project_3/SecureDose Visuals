import streamlit as st
from web3 import Web3
import json
from datetime import datetime


# Setting up the theme of the streamlit app 

# 
st.set_page_config(
    page_title="Drug Authenticity Management",
    page_icon=":pill:", # Populates a pill emoji, we can fill this in with a png or website for a more realistic look 

    layout="wide",
    initial_sidebar_state="expanded",
    theme={
        "primaryColor": "#F63366",
        "backgroundColor": "#FFFFFF",
        "secondaryBackgroundColor": "#F0F2F6",
        "textColor": "#262730",
        "font": "sans-serif"
    }
)

# Input Dashboard data 

# Assuming necessary imports and theme configuration are at the top

# Title
st.title("Drug Authenticity Management")

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Sidebar for contract address and private key
contract_address = st.sidebar.text_input("Contract Address", "0xC628D8B2684517bB25090a6e29dB1c756Cd85845")
private_key = st.sidebar.text_area("Private Key", "0x4edaa67ba1ed37634ae0fee988c1c11452b350fa91b5b6bbb3d8ef56cc30167f")

# Dashboard Section (Replace this with actual data retrieval and processing)
# Example pie chart
company_data = {
    'Verified': 10,  # Replace with actual number of verified companies
    'Unverified': 5   # Replace with actual number of unverified companies
}
st.sidebar.subheader('Company Verification Status')
st.sidebar.pie_chart(company_data)

# Example line chart for drug registration over time
dates = ["Jan", "Feb", "Mar", "Apr", "May"]
registered_drugs = [10, 12, 15, 20, 25]  # Replace with actual drug registration data
st.sidebar.subheader('Drug Registration Over Time')
st.sidebar.line_chart(registered_drugs)


if contract_address and private_key:

    # Load ABI
    with open("contract_abi.json", "r") as f:
        contract_abi = json.load(f)

    # Set up contract
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    sender_address = w3.eth.account.privateKeyToAccount(private_key).address
    st.sidebar.write(f"Connected as {sender_address}")

    # Header
    st.header("Choose a Function")
    option = st.selectbox('', ('verifyCompany', 'revokeVerification', 'registerDrug', 'transferDrug', 'fetchTotalDrugs', 'fetchDrugDetails', 'searchDrugByName'))

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

    #In order to run this, a searchdrugsbyname function needs to be input
    #our smart contract

    # This code should return a list of drug IDs. Depending on the exact implementation 

    # An Option that we need to consider is taking out the private keys 

    elif option == 'searchDrugByName':
        st.subheader("Search for a Drug")
        
        # Search bar for drug names
        drug_name_query = st.text_input("Enter Drug Name to Search")
        
        if st.button("Search"):
            # Assuming you have a function in your contract that returns a list of drug IDs based on a drug name:
            drug_ids = contract.functions.searchDrugsByName(drug_name_query).call()
            
            if drug_ids:
                for drug_id in drug_ids:
                    drug_details = contract.functions.drugs(drug_id).call()
                    st.write(f"Drug ID {drug_id}: {drug_details}")
            else:
                st.write("No drugs found with that name.")

else:
    st.sidebar.write("Please enter the contract address and private key to proceed.")
