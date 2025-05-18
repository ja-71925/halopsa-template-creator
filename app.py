import streamlit as st
import pandas as pd
import tempfile
from TicketTemplates import run_halo_upload

st.set_page_config(page_title="HaloPSA CSV Uploader", layout="centered")

# 🎟️ Stylized Title
st.markdown("<h1 style='text-align: center;'>🎟️ HaloPSA CSV Uploader</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Upload a CSV to automate ticket creation in HaloPSA</p>", unsafe_allow_html=True)

# ---------------- AUTHENTICATION ----------------
VALID_USERS = st.secrets["credentials"]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.authenticated:
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in VALID_USERS and password == VALID_USERS[username]:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success(f"✅ Welcome, {username}! You are now logged in.")
            st.experimental_rerun()
        else:
            st.error("❌ Invalid username or password")

    st.stop()  # Stops execution for unauthenticated users

# ---------------- APP CONTENT ----------------

# Sidebar logout button
with st.sidebar:
    st.write(f"👤 Logged in as: `{st.session_state.username}`")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.experimental_rerun()

st.success(f"🔓 Authenticated as `{st.session_state.username}`")

with st.form("upload_form"):
    st.subheader("🔐 HaloPSA Credentials")
    base_url = st.text_input("API Base URL (e.g. https://api.halopsa.com)")
    oauth_url = st.text_input("OAuth2 Token URL")
    client_id = st.text_input("Client ID")
    client_secret = st.text_input("Client Secret", type="password")

    st.subheader("📄 Upload CSV File")
    uploaded_file = st.file_uploader("Choose your CSV", type=["csv"])

    submitted = st.form_submit_button("🚀 Run Script")

if submitted:
    if not all([base_url, oauth_url, client_id, client_secret, uploaded_file]):
        st.error("Please fill in all fields and upload a CSV file.")
    else:
        try:
            with st.spinner("Processing..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name

                result = run_halo_upload(
                    csv_path=tmp_path,
                    base_url=base_url,
                    oauth_url=oauth_url,
                    client_id=client_id,
                    client_secret=client_secret
                )

            st.success(result)
        except Exception as e:
            st.error(f"❌ Error: {e}")
