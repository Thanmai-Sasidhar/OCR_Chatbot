import streamlit as st
import streamlit_authenticator as stauth
from db import session, ChatHistory

st.set_page_config(page_title="Admin Dashboard", page_icon="🧑‍💼")

# ---- Simple Authentication ----
names = ["Admin"]
usernames = ["admin"]
passwords = ["admin123"]  # change for security

hashed_passwords = stauth.Hasher(passwords).generate()
authenticator = stauth.Authenticate(
    names, usernames, hashed_passwords,
    "chatbot_dashboard", "abcdef", cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.title("🧑‍💼 Chatbot Admin Dashboard")

    st.subheader("💬 All Chat Messages")
    data = session.query(ChatHistory).all()
    if not data:
        st.info("No chat messages found.")
    else:
        for msg in data:
            st.markdown(f"**[{msg.chat_name}] {msg.role.upper()}**: {msg.content}")
            st.caption(f"{msg.timestamp}")

    if st.button("🗑 Clear All Chats"):
        session.query(ChatHistory).delete()
        session.commit()
        st.success("All chats deleted!")

elif authentication_status is False:
    st.error("Invalid username or password.")
else:
    st.warning("Please log in to access the admin panel.")
