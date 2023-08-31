import streamlit as st
from web3 import Web3
import json
from datetime import datetime

import pydeck as pdk
import pandas as pd 

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import streamlit as st
import pydeck as pdk

import streamlit as st
import pydeck as pdk

import streamlit as st
from datetime import datetime
# Setting up the theme of the streamlit app 
st.title("Help Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("How can I help?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Help: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Define a function for each page
# Check if 'page' exists in the session stat
def homepage():
    st.title("SecureDose: Ensuring Authenticity from Manufacturer to Consumer")
    
    # Introduction
    st.write("Welcome to SecureDose, a decentralized platform ensuring the traceability and genuineness of medical drugs. From manufacturers to consumers, every step is logged to guarantee you receive authentic products.")

    # Benefits/Why use
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Why Verify Here?")
        st.write("- Ensure your drug's genuineness.")
        st.write("- Track the origin and journey of your medicine.")
        st.write("- Contribute to a database that helps others stay safe.")

    with col2:
        st.subheader("Safety Tips:")
        st.write("- Always purchase medicines from reputable pharmacies.")
        st.write("- Check the packaging for signs of tampering.")
        st.write("- If in doubt, always consult with a healthcare professional before consumption.")

    # Dropdown with instructions based on role selection
    st.subheader("Select Your Role:")

    role_options = {
        "I'm a Manufacturer": "Manufacturers have the crucial task of introducing genuine medicines to the market. Here, you can verify your company, register new drug products, log batch numbers, and maintain the standard of pharmaceuticals by ensuring traceability. This platform helps manufacturers build trust with both pharmacies and end consumers.",
        "I'm a Pharmacy": "Pharmacies play an essential intermediary role. Here, you can verify drug receipts, log sales, and ensure the chain of custody remains unbroken. This platform helps pharmacies assure customers of the authenticity of the drugs they sell.",
        "I'm a Consumer": "Consumers need assurance of drug safety and authenticity. Here, you can verify the journey of your drug from the manufacturer to the pharmacy. This platform lets you be sure you're getting genuine products."
    }

    role_selection = st.selectbox("Choose a Role", list(role_options.keys()), key="homepage_role_selection")
    st.write(role_options[role_selection])

    # Button to navigate to the respective page based on dropdown selection
    if st.button("Proceed to " + role_selection):
        st.session_state.page = role_selection

    # Outside the function (At the root level of your script
    if st.session_state.page == 'homepage':
        homepage()
    elif st.session_state.page == "I'm a Manufacturer":
        manufacturer_page()  # Assuming you've defined this function
    elif st.session_state.page == "I'm a Pharmacy":
        pharmacy_page()  # Assuming you've defined this function
    elif st.session_state.page == "I'm a Consumer":
        customer_page()  # Assuming you've defined this function


def analytics():
    import streamlit as st
    import pandas as pd
    import numpy as np
    import datetime
    import plotly.express as px

    st.header("Analytics Page")
    st.write("Here you can see all the analytics related to our app.")

    # Check if dataset is already in session state
    if 'data_df' not in st.session_state:
        # Dummy Data (This can be replaced with your actual initialization logic)
        data = {
            'DrugID': [f'D00{i}' for i in range(1, 101)],
            'RegistrationDate': [(datetime.datetime.now() - datetime.timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d') for _ in range(100)],
            'Company': ['Company A', 'Company B', 'Company C', 'Company D', 'Company E'] * 20,
            'TransferCount': np.random.randint(1, 50, 100),
            'ExpiryDate': [(datetime.datetime.now() + datetime.timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d') for _ in range(100)],
        }
        st.session_state.data_df = pd.DataFrame(data)
    
    df = st.session_state.data_df

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

    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'drug_id_entered' not in st.session_state:
        st.session_state.drug_id_entered = False
    if 'date_entered' not in st.session_state:
        st.session_state.date_entered = False
    if 'pharmacy_address_entered' not in st.session_state:
        st.session_state.pharmacy_address_entered = False

    # Task 1: Login
    if not st.session_state.logged_in:
        st.subheader("Login")
        username = st.text_input("Username", key='username_input')
        password = st.text_input("Password", key='password_input', type='password')
        if st.button('Login'):
            if username and password:  # Add your actual logic for login verification here
                st.session_state.logged_in = True
                st.success("Logged in successfully!")

    # Task 2: Enter Drug ID
    elif not st.session_state.drug_id_entered:
        st.subheader("Enter Drug ID received")
        drug_id = st.text_input("Drug ID", key='drug_id_input')
        if drug_id:
            st.session_state.drug_id_entered = True
            st.success("Drug ID entered!")

    # Task 3: Date Received
    elif not st.session_state.date_entered:
        st.subheader("Date you received")
        date_received = st.date_input("Select a date", key='date_received_input')
        if date_received:
            st.session_state.date_entered = True
            st.success("Date entered!")

    # Task 4: Pharmacy Address
    elif not st.session_state.pharmacy_address_entered:
        st.subheader("Pharmacy Address")
        pharmacy_address = st.text_input("Pharmacy Address", key='pharmacy_address_input')
        if pharmacy_address:
            st.session_state.pharmacy_address_entered = True
            st.success("Pharmacy address entered!")

    # Final completion
    if st.session_state.pharmacy_address_entered:
        st.write("Thank you for verifying")
        if st.button("Enter another drug ID?"):
            # Reset session state values
            st.session_state.logged_in = False
            st.session_state.drug_id_entered = False
            st.session_state.date_entered = False
            st.session_state.pharmacy_address_entered = False

def send_transaction(tx):
    # Placeholder for your send_transaction function
    pass

def manufacturer_page():
    st.title("Manufacturer Page")
    
    # Initialize session state
    if 'wallet_verified' not in st.session_state:
        st.session_state.wallet_verified = False
    if 'company_verified' not in st.session_state:
        st.session_state.company_verified = False
    if 'drug_registered' not in st.session_state:
        st.session_state.drug_registered = False
    if 'drug_transferred' not in st.session_state:
        st.session_state.drug_transferred = False

    # Task 1: Wallet Verification
    if not st.session_state.wallet_verified:
        st.subheader("Wallet Verification")
        wallet_address = st.text_input("Please verify Wallet Address", key='wallet_address_input')
        if wallet_address:
            # ... Add your logic for verifying the wallet ...
            st.session_state.wallet_verified = True

    # Task 2: Verify Company
    elif not st.session_state.company_verified:
        st.subheader("Verify Company")
        company_address = st.text_input("Company Address to Verify", key='company_address_input')
        if st.button("Submit Company Verification"):
            tx = contract.functions.verifyCompany(company_address).buildTransaction({
                'gas': 2000000,
                'gasPrice': w3.toWei('40', 'gwei'),
                'nonce': w3.eth.getTransactionCount(sender_address),
            })
            send_transaction(tx)
            st.session_state.company_verified = True

    # Task 3: Register Drug
    elif not st.session_state.drug_registered:
        st.subheader("Register Drug")
        name = st.text_input("Drug Name", key='drug_name_input')
        components = st.text_input("Components (comma-separated)", key='components_input')
        manufacture_date = st.date_input("Manufacture Date")
        expiry_date = st.date_input("Expiry Date")
        description = st.text_area("Description", key='description_input')
        token_uri = st.text_input("Token URI", key='token_uri_input')

        manufacture_timestamp = datetime.combine(manufacture_date, datetime.min.time()).timestamp()
        expiry_timestamp = datetime.combine(expiry_date, datetime.min.time()).timestamp()

        if st.button("Submit Drug Registration"):
            tx = contract.functions.registerDrug(name, components, int(manufacture_timestamp), int(expiry_timestamp), description, token_uri).buildTransaction({
                'gas': 2000000,
                'gasPrice': w3.toWei('40', 'gwei'),
                'nonce': w3.eth.getTransactionCount(sender_address),
            })
            send_transaction(tx)
            st.session_state.drug_registered = True

    # Task 4: Transfer Drug
    elif not st.session_state.drug_transferred:
        st.subheader("Transfer Drug")
        drug_id = st.number_input("Enter Drug ID to transfer", min_value=1, value=1, step=1, key='drug_id_input')
        to_address = st.text_input("Enter recipient's address", key='recipient_address_input')
        if st.button("Submit Drug Transfer"):
            tx = contract.functions.transferDrug(drug_id, to_address).buildTransaction({
                'gas': 2000000,
                'gasPrice': w3.toWei('40', 'gwei'),
                'nonce': w3.eth.getTransactionCount(sender_address),
            })
            send_transaction(tx)
            st.session_state.drug_transferred = True

    if st.session_state.drug_transferred:
        st.markdown("✅ Sent Successfully!")
        st.write("You have successfully completed all tasks!")
        if st.button("Submit Another Drug"):
            # Reset session state values
            st.session_state.wallet_verified = False
            st.session_state.company_verified = False
            st.session_state.drug_registered = False
            st.session_state.drug_transferred = False


def send_transaction(tx):
    # Placeholder function to send transactions.
    # This should be replaced with the actual method to interact with the Ethereum network.
    pass

def pharmacy_page():
    st.title("SecureDose Pharmacy")

    # Initialize session state for drug inventory, locations, and verification
    if 'drug_inventory' not in st.session_state:
        st.session_state.drug_inventory = {}
    if 'location_info' not in st.session_state:
        st.session_state.location_info = []
    if 'wallet_verified' not in st.session_state:
        st.session_state.wallet_verified = False

    role = st.selectbox("Choose a role", ["Pharmacy"])
    if role == "Pharmacy":

        # Wallet Verification
        if not st.session_state.wallet_verified:
            st.subheader("Wallet Verification")
            wallet_address = st.text_input("Enter Wallet Address for Verification", key="wallet_verification")
            if st.button("Verify Wallet"):
                # This is a mock verification for the demo. Replace with actual verification.
                if wallet_address:  
                    st.session_state.wallet_verified = True
                    st.write("Wallet Verified Successfully!")
                else:
                    st.write("Invalid Wallet Address!")

        # If wallet is verified, proceed with other tasks
        elif st.session_state.wallet_verified:
            # Register Drug Section
            st.subheader("Register Drug")
            drug_name = st.text_input("Drug Name", key='pharmacy_drug_name_input')
            if drug_name:
                st.session_state.drug_inventory[drug_name] = st.session_state.drug_inventory.get(drug_name, 0) + 1

                # Mockup for recording location based on wallet address.
                # Here, for demonstration purposes, we'll use dummy latitude and longitude.
                # This is assuming a function or method to fetch coordinates based on a wallet address.
                lat, lon = 40.730610, -73.935242  # Replace with actual location data.
                st.session_state.location_info.append({"lat": lat, "lon": lon, "drug": drug_name})

                st.write(f"Registered {drug_name} into the inventory.")

            # Transfer Drug Section
            st.subheader("Transfer Drug")
            drug_name_transfer = st.text_input("Drug Name to Transfer", key='pharmacy_drug_transfer_input')
            recipient_name = st.text_input("Recipient Name")
            if st.button("Confirm Drug Transfer"):
                if drug_name_transfer in st.session_state.drug_inventory and st.session_state.drug_inventory[drug_name_transfer] > 0:
                    st.session_state.drug_inventory[drug_name_transfer] -= 1
                    st.write(f"Transferred {drug_name_transfer} to {recipient_name}.")
                else:
                    st.write(f"{drug_name_transfer} not in stock or insufficient stock.")

            # Map of drug registrations based on location
            st.subheader("Drug Registration Locations")
            map_data = pd.DataFrame(st.session_state.location_info)
            if not map_data.empty:
                st.pydeck_chart(pdk.Deck(
                    map_style='mapbox://styles/mapbox/light-v9',
                    initial_view_state=pdk.ViewState(
                        latitude=40.730610,
                        longitude=-73.935242,
                        zoom=12,
                        pitch=0,
                    ),
                    layers=[
                        pdk.Layer(
                            'ScatterplotLayer',
                            data=map_data,
                            get_position='[lon, lat]',
                            get_radius=100,
                            get_fill_color='[200, 30, 0, 160]',
                            pickable=True,
                            auto_highlight=True,
                        ),
                    ],
                ))






pages = {
    "Homepage": homepage,
    "Customer Page": customer_page,
    "Manufacturer Page": manufacturer_page,
    "Pharmacy Page": pharmacy_page,
    "Analytics": analytics,
}

# def main():
#     st.sidebar.title("Navigation")
#     page = st.sidebar.selectbox("Choose a page:", list(pages.keys()))

#     pages[page]()

# if __name__ == "__main__":
#     main()

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
