from fastapi import HTTPException, status
from firebase_admin import auth


async def create_user(email, password):
    try:
        user = auth.create_user(
            email=email,
            password=password,
        )
    except auth.EmailAlreadyExistsError:
        print("User already exists")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",  # noqa
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error as {e}"
        )  # noqa

    return user.uid if user else None


async def change_password(user_id, new_password):
    try:
        auth.update_user(
            user_id=user_id,
            password=new_password,
        )
        return True
    except Exception as e:
        print(f"Error updating user password: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            details=f"Error updating user password: {e}",
        )
        return False


async def create_user_by_mobile(mobile):
    try:
        user = auth.create_user(
            phone_number=mobile,
        )
    except auth.PhoneNumberAlreadyExistsError:
        print("User already exists")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error as {e}",
        )
    return user.uid if user else None


async def change_mobile_number(user_id, new_mobile_number):
    user_data = {"phone_number": new_mobile_number}
    try:
        auth.update_user(user_id, **user_data)
        return True
    except Exception as e:
        print(f"Error updating user phonenumber: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating phonenumber: {e}",
        )
        return False


async def delete_user(uid):
    try:
        auth.delete_user(uid)
    except Exception as e:
        print(f"Error deleteing user: {e}")


async def revoke_refresh_token(uid):
    try:
        auth.revoke_refresh_token(uid)
    except Exception as e:
        print(f"Error revoking refresh token: {e}")
