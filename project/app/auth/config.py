import firebase_admin
from firebase_admin import credentials, initialize_app

# Path to your Firebase service account key file
firebase_key_file = "./firebase_service_account.json"

# Load credentials from JSON file
cred = credentials.Certificate(firebase_key_file)


async def firebase_init():
    if not firebase_admin._apps:
        initialize_app(cred)
