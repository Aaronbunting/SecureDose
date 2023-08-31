import streamlit as st
from web3 import Web3
import json
from datetime import datetime

import pydeck as pdk
import pandas as pd 

# Setting up the theme of the streamlit app 


# Define a function for each page
def homepage():
    import streamlit as st
    st.header("Welcome to the Homepage!")
    st.image('./ambulance.jpg', width = 700)
    st.title("Drug Authenticity Management")

    st.title("Bar with Role-Based Tasks")

    role = st.selectbox(
    "Choose a role",
    ("Manufacturer", "Customer")
    )


    tasks = []

    if role == "Manufacturer":
        st.subheader("Manufacturer Tasks")
        # Verify Company Task
        verify_company = st.checkbox("Verify Company")
        if verify_company:
            company_address = st.text_input("Company Address to Verify")
            if st.button("Submit Company Verification"):
                tx = contract.functions.verifyCompany(company_address).buildTransaction({
                    'gas': 2000000,
                    'gasPrice': w3.toWei('40', 'gwei'),
                    'nonce': w3.eth.getTransactionCount(sender_address),
                })
                send_transaction(tx)

    # Register Drug Task
        register_drug = st.checkbox("Register Drug")
        if register_drug:
            name = st.text_input("Drug Name")
            components = st.text_input("Components (comma-separated)")
            manufacture_date = st.date_input("Manufacture Date")
            expiry_date = st.date_input("Expiry Date")
            description = st.text_area("Description")
            token_uri = st.text_input("Token URI")

            manufacture_timestamp = datetime.combine(manufacture_date, datetime.min.time()).timestamp()
            expiry_timestamp = datetime.combine(expiry_date, datetime.min.time()).timestamp()

            if st.button("Submit Drug Registration"):
                tx = contract.functions.registerDrug(name, components, int(manufacture_timestamp), int(expiry_timestamp), description, token_uri).buildTransaction({
                    'gas': 2000000,
                    'gasPrice': w3.toWei('40', 'gwei'),
                    'nonce': w3.eth.getTransactionCount(sender_address),
                })
                send_transaction(tx)

    # Transfer Drug Task
        transfer_drug = st.checkbox("Transfer Drug")
        if transfer_drug:
            drug_id = st.number_input("Enter Drug ID to transfer", min_value=1, value=1, step=1)
            to_address = st.text_input("Enter recipient's address")
        
            if st.button("Submit Drug Transfer"):
                tx = contract.functions.transferDrug(drug_id, to_address).buildTransaction({
                    'gas': 2000000,
                    'gasPrice': w3.toWei('40', 'gwei'),
                    'nonce': w3.eth.getTransactionCount(sender_address),
                })
                send_transaction(tx)

        tasks.append(("Verify Company", verify_company))
        tasks.append(("Register Drug", register_drug))
        tasks.append(("Transfer Drug", transfer_drug))

    
    elif role == "Customer":
        st.subheader("Customer Tasks")
        confirmed_purchase = st.checkbox("Confirmed Purchase")
        confirmed_drug = st.checkbox("Confirmed Drug")
    
        tasks.append(("Confirmed Purchase", confirmed_purchase))
        tasks.append(("Confirmed Drug", confirmed_drug))

    progress_percentage = show_progress(tasks)

    if progress_percentage == 1.0:
        st.write("All tasks completed! 🎉")

def analytics():
    import streamlit as st
    import pandas as pd
    import numpy as np
    import datetime
    import plotly.express as px

    st.header("Analytics Page")
    st.write("Here you can see all the analytics related to our app.")

    # Dummy Data
    data = {
        'DrugID': [f'D00{i}' for i in range(1, 101)],
        'RegistrationDate': [(datetime.datetime.now() - datetime.timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d') for _ in range(100)],
        'Company': ['Company A', 'Company B', 'Company C', 'Company D', 'Company E'] * 20,
        'TransferCount': np.random.randint(1, 50, 100),
        'ExpiryDate': [(datetime.datetime.now() + datetime.timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d') for _ in range(100)],
    }

    df = pd.DataFrame(data)
    df['RegistrationDate'] = pd.to_datetime(df['RegistrationDate'])
    df['ExpiryDate'] = pd.to_datetime(df['ExpiryDate'])

    # Overview Metrics & Company Insights
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Overview Metrics")
        total_drugs = df['DrugID'].nunique()
        total_companies = df['Company'].nunique()
        st.write(f"Total Drugs Registered: **{total_drugs}**")
        st.write(f"Total Companies: **{total_companies}**")

    with col2:
        st.subheader("Company Insights")
        company_counts = df['Company'].value_counts()
        fig = px.bar(x=company_counts.index, y=company_counts.values, title='Drug Registrations by Company')
        st.plotly_chart(fig)

    # Drug Registration Trends & Top Drugs by Transfer Activity
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Drug Registration Trends")
        fig = px.histogram(df, x='RegistrationDate', title='Drug Registrations Over Time', nbins=12)
        st.plotly_chart(fig)

    with col4:
        st.subheader("Top Drugs by Transfer Activity")
        top_drugs = df.sort_values(by='TransferCount', ascending=False).head(10)
        st.write(top_drugs[['DrugID', 'TransferCount']])

    # Drugs Nearing Expiry & Search and Filter Options
    col5, col6 = st.columns(2)
    with col5:
        st.subheader("Drugs Nearing Expiry")
        near_expiry = df[df['ExpiryDate'] <= (datetime.datetime.now() + datetime.timedelta(days=60))]
        st.write(near_expiry[['DrugID', 'ExpiryDate']])

    with col6:
        st.subheader("Search & Filter Options")
        search_term = st.text_input("Search for a Drug by ID")
        if search_term:
            results = df[df['DrugID'] == search_term]
            st.write(results)

    # Example line chart for drug registration over time in the sidebar
    dates = ["Jan", "Feb", "Mar", "Apr", "May"]
    registered_drugs = [10, 12, 15, 20, 25]  # Replace with actual drug registration data
    st.sidebar.subheader('Drug Registration Over Time')
    st.sidebar.line_chart(registered_drugs)

def customer_page():
    st.title("Customer Page")
    st.write("Content for customers goes here.")

def manufacturer_page():
    st.title("Manufacturer Page")
    st.write("Content for manufacturers goes here.")

def pharmacy_page():
    st.title("Pharmacy Page")
    st.write("Content for pharmacies goes here.")

def feedback_page():
    st.title("Feedback Page")
    feedback_text = st.text_area("Please provide your feedback here...")
    if st.button("Submit"):
        st.write("Thank you for your feedback!")

def settings():
    st.header("Settings Page")
    st.write("Adjust the settings of the app here.")

pages = {
    "Homepage": homepage,
    "Customer Page": customer_page,
    "Manufacturer Page": manufacturer_page,
    "Pharmacy Page": pharmacy_page,
    "Feedback Page": feedback_page,
    "Analytics": analytics,
    "Settings": settings
}

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page:", list(pages.keys()))

    pages[page]()

if __name__ == "__main__":
    main()

# Sidebar selectbox for navigation
page = st.sidebar.selectbox("Choose a page:", list(pages.keys()))

# Call the function to display the selected page
pages[page]()
#___________________________________________________________________________________________________________________________________________________

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Sidebar for contract address and private key
contract_address = st.sidebar.text_input("Contract Address", "0xC628D8B2684517bB25090a6e29dB1c756Cd85845")
private_key = st.sidebar.text_area("Private Key", "0x4edaa67ba1ed37634ae0fee988c1c11452b350fa91b5b6bbb3d8ef56cc30167f")

#________________________________________________________________________________________________________________________________________________________________________________________

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
else:
    st.sidebar.write("Please enter the contract address and private key to proceed.")

