import streamlit as st

# ------------------ Setup ------------------
# Initialize session state for storage and attempts
if 'stored_data' not in st.session_state:
    st.session_state.stored_data = {}

if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0

# ------------------ Caesar Cipher Functions ------------------

# Basic Caesar cipher encryption
def caesar_encrypt(text, shift=3):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

# Basic Caesar cipher decryption
def caesar_decrypt(text, shift=3):
    return caesar_encrypt(text, -shift)

# ------------------ Decryption Function ------------------

def decrypt_data(encrypted_text, passkey):
    for key, value in st.session_state.stored_data.items():
        if key == encrypted_text and value['passkey'] == passkey:
            st.session_state.failed_attempts = 0
            return caesar_decrypt(value['encrypted_text'])
    st.session_state.failed_attempts += 1
    return None

# ------------------ Streamlit UI ------------------

st.set_page_config(page_title="Secure Caesar Cipher", page_icon="🔐")
st.title("🛡️ Simple Secure Data System (No External Libraries)")

menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("🔍 Navigation", menu)

# ------------------ Home ------------------
if choice == "Home":
    st.subheader("🏠 Welcome!")
    st.write("This app uses a **simple Caesar cipher** to store and retrieve encrypted data using a passkey.")

# ------------------ Store Data ------------------
elif choice == "Store Data":
    st.subheader("📂 Store Your Data")
    user_data = st.text_area("Enter the data to encrypt:")
    passkey = st.text_input("Create a passkey:", type="password")

    if st.button("Encrypt & Store"):
        if user_data and passkey:
            encrypted_text = caesar_encrypt(user_data)
            st.session_state.stored_data[encrypted_text] = {
                "encrypted_text": encrypted_text,
                "passkey": passkey
            }
            st.success("✅ Data encrypted and stored!")
            st.write("🔐 Save this encrypted data securely:")
            st.code(encrypted_text)
        else:
            st.error("⚠️ Both fields are required!")

# ------------------ Retrieve Data ------------------
elif choice == "Retrieve Data":
    st.subheader("🔓 Retrieve Your Data")
    encrypted_input = st.text_area("Enter your encrypted data:")
    passkey = st.text_input("Enter your passkey:", type="password")

    if st.button("Decrypt"):
        if encrypted_input and passkey:
            result = decrypt_data(encrypted_input, passkey)

            if result:
                st.success("✅ Decrypted Data:")
                st.code(result)
            else:
                remaining = 3 - st.session_state.failed_attempts
                st.error(f"❌ Incorrect passkey! Attempts left: {remaining}")
                if st.session_state.failed_attempts >= 3:
                    st.warning("🔒 Too many failed attempts. Redirecting to Login...")
                    st.experimental_rerun()
        else:
            st.error("⚠️ Both fields are required!")

# ------------------ Login Page ------------------
elif choice == "Login":
    st.subheader("🔑 Reauthorization")
    login_pass = st.text_input("Enter master password:", type="password")

    if st.button("Login"):
        if login_pass == "admin123":  # Simple demo login
            st.session_state.failed_attempts = 0
            st.success("✅ Reauthorized! You may now try again.")
            st.experimental_rerun()
        else:
            st.error("❌ Incorrect master password.")
