import streamlit as st
import pandas as pd
import tempfile
from TicketTemplates import run_halo_upload

# ---------- LOGIN PROTECTION ----------
st.set_page_config(page_title="🎟️ HaloPSA CSV Uploader", layout="centered")
st.title("🎟️ HaloPSA CSV Uploader")

# Dummy login credentials
VALID_PASSWORD = "msp123"

# Check session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Show login form if not authenticated
if not st.session_state.authenticated:
    st.subheader("Please login to continue")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if password == VALID_PASSWORD:
            st.session_state.authenticated = True
            st.experimental_rerun()
        else:
            st.error("❌ Incorrect password")
    st.stop()  # Stop the app here if not logged in

# ---------- AUTHENTICATED AREA ----------
st.success("✅ Logged in successfully!")

with st.form("upload_form"):
    st.subheader("🔐 HaloPSA Credentials")
    base_url = st.text_input("API Base URL (e.g. https://example.halopsa.com/api)")
    oauth_url = st.text_input("OAuth2 Token URL (e.g. https://example.halopsa.com/auth/token)")
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
