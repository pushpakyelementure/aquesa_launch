from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import verify
# from app.routers.auth.auth_doc_res import logout
from app.routers.auth import auth_res_schema
from app.routers.auth import auth_crud

router = APIRouter()


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    response_model=auth_res_schema.logout_response,
    # responses=logout.responses
    )
async def logout_user(
    user_token=Depends(verify.get_user_token),
):
    try:
        # buisness logic
        await auth_crud.log_out(user_token=user_token)
        return {
            "detail": "logout successfully",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
