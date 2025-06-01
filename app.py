import streamlit as st
import streamlit_authenticator as stauth
import tempfile
from TicketTemplates import run_halo_upload

# ---------- Safely load secrets ----------
credentials = {k: dict(v) for k, v in st.secrets["credentials"].items()}
cookie = dict(st.secrets["cookie"])

config = {
    "credentials": {"usernames": credentials},
    "cookie": cookie
}

# ---------- Authentication ----------
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, auth_status, username = authenticator.login("Login", "main")

if auth_status:
    st.session_state.username = username
    user_info = config["credentials"]["usernames"][username]
    role = user_info.get("role", "user")

    st.sidebar.success(f"👤 Logged in as {username} ({role})")
    authenticator.logout("Logout", "sidebar")

elif auth_status is False:
    st.error("❌ Invalid username or password")
    st.stop()
else:
    st.warning("Please enter your credentials.")
    st.stop()

# ---------- Main App Interface ----------
st.markdown("<h1 style='text-align: center;'>🎟️ HaloPSA CSV Uploader</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Upload a CSV to automate ticket templates creation in HaloPSA</p>", unsafe_allow_html=True)

with st.form("upload_form"):
    st.subheader("🔐 HaloPSA Credentials")
    base_url = st.text_input("API Base URL")
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