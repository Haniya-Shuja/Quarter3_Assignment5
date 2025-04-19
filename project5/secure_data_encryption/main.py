
import streamlit as st
import hashlib
import os
import json

# --- Key Management ---
# Removed KEY_FILE and load_key as Fernet is no longer used

# --- Data Storage ---
DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# --- Helpers ---
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# Removed encrypt_data and decrypt_data functions

# --- Session State Init ---
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

stored_data = load_data()

# --- UI Starts ---
st.title("🔐 Data Storage App")


menu = ['Home', 'Store Data', 'Retrieve Data', 'Login']
choice = st.sidebar.radio('Navigation', menu)

# --- HOME ---
if choice == "Home":
    st.subheader('🏠 Welcome')
    st.write('This app stores and retrieves data.')

# --- LOGIN ---
elif choice == "Login":
    st.subheader("🔑 Login to Access Data")

    username = st.text_input("Enter any username")  # can be used for further expansion
    login_pass = st.text_input("Enter passkey", type='password')

    if st.button("Login"):
        # No strict login in this version; just enables storing/retrieving
        if login_pass:
            st.session_state.is_logged_in = True
            st.success("Logged in successfully.")
        else:
            st.session_state.failed_attempts += 1
            st.error("Please enter a valid passkey.")

# --- STORE DATA ---
elif choice == "Store Data":
    if not st.session_state.is_logged_in:
        st.warning("Please login to store data.")
    else:
        st.subheader("📝 Store Data")

        label = st.text_input('Label your data (e.g., Note1)')
        plain_text = st.text_area('Enter your data')
        passkey = st.text_input('Set a passkey', type='password')

        if st.button('Store Data'):
            if label and plain_text and passkey:
                hashed_key = hash_passkey(passkey)

                stored_data[label] = {
                    'plain_text': plain_text,
                    'pass_key': hashed_key
                }

                save_data(stored_data)
                st.success('✅ Data stored successfully .')
            else:
                st.warning("Please fill in all fields.")

# --- RETRIEVE DATA ---
elif choice == "Retrieve Data":
    if not st.session_state.is_logged_in:
        st.warning("Please login to retrieve data.")
    else:
        st.subheader("🔍 Retrieve Your Data")

        label = st.text_input("Enter the label of your stored data")
        passkey = st.text_input("Enter your passkey", type='password')

        if st.button("Retrieve"):
            if label in stored_data:
                stored_entry = stored_data[label]
                hashed_input_key = hash_passkey(passkey)

                if hashed_input_key == stored_entry['pass_key']:
                    retrieved_data = stored_entry['plain_text']
                    st.success("✅ Data retrieved successfully:")
                    st.text_area("Retrieved Data", retrieved_data, height=150)
                else:
                    st.error("❌ Incorrect passkey.")
            else:
                st.error("❌ No data found with that label.")