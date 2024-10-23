import os
import pyrebase

config = {
    "apiKey": os.getenv("FB_CLIENT_API_KEY"),
    "authDomain": os.getenv("FB_CLIENT_AUTH_DOMAIN"),
    "projectId": os.getenv("FB_CLIENT_PROJECT_ID"),
    "storageBucket": os.getenv("FB_CLIENT_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FB_CLIENT_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FB_CLIENT_APP_ID"),
    "measurementId": os.getenv("FB_CLIENT_MEASUREMENT_ID"),
    "databaseURL": "https://none.firebaseio.com",
}

firebase = pyrebase.initialize_app(config)


def login_and_get_id_token(email, password):
    try:
        # Sign in the user with email and password
        user = firebase.auth().sign_in_with_email_and_password(email, password)

        # Get the ID token from the user
        id_token = user["idToken"]
        refresh_token = user["refreshToken"]

        print(f"ID Token: {id_token}")
        print(f"Refresh Token: {refresh_token}")

        return id_token
    except Exception as err:
        print(f"Failed to login with email: {email}")
        print(f"Details of Error as {err}")
        return None


login_and_get_id_token(
    os.getenv("FIREBASE_SUPERUSER_ADMIN_EMAIL"),
    os.getenv("FIREBASE_SUPERUSER_ADMIN_PASSWORD"),
)
