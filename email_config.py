from cryptography.fernet import Fernet
import json

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def save_email_config(sender_email, app_password, receiver_email):
    with open("secret.key", "rb") as key_file:
        key = key_file.read()
    fernet = Fernet(key)

    credentials = {
        "sender": sender_email,
        "password": fernet.encrypt(app_password.encode()).decode(),
        "receiver": receiver_email
    }

    with open("email_config.json", "w") as f:
        json.dump(credentials, f)

# generate_key()
# save_email_config("muditmohitkumarsingh@gmail.com", "fpzt lele ztod cafb", "mudit.mohit21@st.niituniversity.in")