from fastapi import HTTPException, status

from app.db.models.admin_user import admin_user_model, user_roles, user_status


async def user_is_superuser_or_admin(user_token):
    token_user = await admin_user_model.find_one(
        admin_user_model.user_id == user_token["uid"]
    )

    if token_user.user_status == user_status.active:
        authorized_roles = [
            user_roles.superuser,
            user_roles.admin,
        ]
        for role in token_user.role:
            if role in authorized_roles:
                return True
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User is not Authorized",
                )
                return False


async def user_is_superuser(user_token):
    token_user = await admin_user_model.find_one(
        admin_user_model.user_id == user_token["uid"]
    )
    if token_user.user_status == user_status.active:
        authorized_roles = [
            user_roles.superuser,
        ]
        for role in token_user.role:
            print(role)
            if role in authorized_roles:
                return True
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User is not authorized"
                )
                return False


async def user_is_superuser_or_admin_or_support(user_token):
    token_user = await admin_user_model.find_one(
        admin_user_model.user_id == user_token["uid"]
    )
    if token_user.user_status == user_status.active:
        authorized_roles = [
            user_roles.superuser,
            user_roles.admin,
            user_roles.support
        ]
        for role in token_user.role:
            print(role)
            if role in authorized_roles:
                return True
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User is not authorized"
                )
                return False


async def user_is_superuser_or_admin_or_support_or_field(user_token):
    token_user = await admin_user_model.find_one(
        admin_user_model.user_id == user_token["uid"]
    )
    if token_user.user_status == user_status.active:
        authorized_roles = [
            user_roles.superuser,
            user_roles.admin,
            user_roles.support,
            user_roles.field
        ]
        for role in token_user.role:
            print(role)
            if role in authorized_roles:
                return True
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User is not authorized"
                )
                return False
