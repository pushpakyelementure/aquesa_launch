import base64
import os

import bcrypt


async def hash_password(password):
    pepper = os.environ.get("PASSWORD_PEPPER")
    password_with_pepper = password + pepper

    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(password_with_pepper.encode(), salt)
    hashed_str = base64.b64encode(hashed).decode()

    return hashed_str


async def verify_password(stored_password_hash, provided_password):
    pepper = os.environ.get("PASSWORD_PEPPER")
    password_with_pepper = provided_password + pepper

    stored_password_bytes = base64.b64encode(stored_password_hash)

    return bcrypt.checkpw(password_with_pepper.encode(), stored_password_bytes)
