from fastapi import Depends, HTTPException, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth


def get_user_token(
    res: Response,
    credential: HTTPAuthorizationCredentials = Depends(
        HTTPBearer(
            auto_error=False,
        )
    ),
):
    if credential is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication is needed",
            headers={"www-authenticate": 'Bearer realm="auth_required"'},
        )
    try:
        decoded_token = auth.verify_id_token(credential.credentials)
        pass
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication from firebase. {err}",
            headers={"www-authenticate": 'Bearer error="invalid_token"'},
        )
    res.headers["www-authenticate"] = 'Bearer realm="auth_required"'
    return decoded_token
