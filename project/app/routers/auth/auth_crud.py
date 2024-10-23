from app.auth import manage


async def log_out(user_token):
    await manage.revoke_refresh_token(user_token["uid"])
