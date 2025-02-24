import os
import pyrebase
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "-s",
    "--superuser",
    help="Generates Super User Token",
)

parser.add_argument(
    "-a",
    "--admin",
    help="Generates Admin User Token",
)

parser.add_argument(
    "-sa",
    "--superuser_admin",
    help="Generates Super User Token",
)

parser.add_argument(
    "-cu",
    "--community_user",
    help="Generates Community User Token",
)

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


args = parser.parse_args()


if args.superuser:
    print("superuser")
    login_and_get_id_token(
        os.getenv("FIREBASE_SUPERUSER_EMAIL"),
        os.getenv("FIREBASE_SUPERUSER_PASSWORD"),
    )

if args.admin:
    print("admin")
    login_and_get_id_token(
        os.getenv("FIREBASE_ADMIN_EMAIL"),
        os.getenv("FIREBASE_ADMIN_PASSWORD"),
    )

if args.superuser_admin:
    print("superuser")
    login_and_get_id_token(
        os.getenv("FIREBASE_SUPERUSER_ADMIN_EMAIL"),
        os.getenv("FIREBASE_SUPERUSER_ADMIN_PASSWORD"),
    )

if args.community_user:
    print("community_user")
    login_and_get_id_token(
        os.getenv("FIREBASE_COMMUNITY_USER_EMAIL"),
        os.getenv("FIREBASE_COMMUNITY_USER_PASSWORD"),
    )