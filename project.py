import streamlit as st
import hashlib
from cryptography.fernet import Fernet

# ------------------ Setup ------------------
# Generate a key for Fernet (should be saved securely in real apps)
KEY = Fernet.generate_key()
cipher = Fernet(KEY)

# Initialize session state for storage and attempts
if 'stored_data' not in st.session_state:
    st.session_state.stored_data = {}

if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0

# ------------------ Utility Functions ------------------

# Hash the user's passkey
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# Encrypt data
def encrypt_data(data):
    return cipher.encrypt(data.encode()).decode()

# Decrypt data (only if passkey matches)
def decrypt_data(encrypted_text, passkey):
    hashed_pass = hash_passkey(passkey)

    if encrypted_text in st.session_state.stored_data:
        saved = st.session_state.stored_data[encrypted_text]
        if saved['passkey'] == hashed_pass:
            st.session_state.failed_attempts = 0  # Reset counter
            return cipher.decrypt(encrypted_text.encode()).decode()

    st.session_state.failed_attempts += 1
    return None

# ------------------ Streamlit UI ------------------

st.set_page_config(page_title="Secure Encryption System", page_icon="🔐")
st.title("🛡️ Secure Data Encryption System")

menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("🔍 Navigation", menu)

# ------------- Home -------------
if choice == "Home":
    st.subheader("🏠 Welcome!")
    st.markdown("Use this app to **securely store and retrieve data** with encryption and passkey protection.")

# ------------- Store Data -------------
elif choice == "Store Data":
    st.subheader("📂 Store Your Data")
    user_data = st.text_area("Enter the data to encrypt:")
    passkey = st.text_input("Create a passkey:", type="password")

    if st.button("Encrypt & Store"):
        if user_data and passkey:
            hashed_pass = hash_passkey(passkey)
            encrypted_text = encrypt_data(user_data)

            # Save encrypted text and passkey hash
            st.session_state.stored_data[encrypted_text] = {
                "encrypted_text": encrypted_text,
                "passkey": hashed_pass
            }

            st.success("✅ Data encrypted and stored successfully!")
            st.write("🔐 Save this encrypted data securely:")
            st.code(encrypted_text)
        else:
            st.error("⚠️ Both fields are required!")

# ------------- Retrieve Data -------------
elif choice == "Retrieve Data":
    st.subheader("🔍 Retrieve Your Data")
    encrypted_text = st.text_area("Enter your encrypted data:")
    passkey = st.text_input("Enter your passkey:", type="password")

    if st.button("Decrypt"):
        if encrypted_text and passkey:
            result = decrypt_data(encrypted_text, passkey)

            if result:
                st.success("✅ Decrypted Data:")
                st.code(result)
            else:
                attempts_left = 3 - st.session_state.failed_attempts
                st.error(f"❌ Incorrect passkey! Attempts left: {attempts_left}")

                if st.session_state.failed_attempts >= 3:
                    st.warning("🔒 Too many failed attempts. Redirecting to Login...")
                    st.experimental_rerun()
        else:
            st.error("⚠️ Both fields are required!")

# ------------- Login Page -------------
elif choice == "Login":
    st.subheader("🔐 Login Required")
    login_input = st.text_input("Enter master password:", type="password")

    if st.button("Login"):
        if login_input == "admin123":  # Replace with secure auth in production
            st.session_state.failed_attempts = 0
            st.success("✅ Reauthorization successful. You can now try again.")
            st.experimental_rerun()
        else:
            st.error("❌ Incorrect master password.")
