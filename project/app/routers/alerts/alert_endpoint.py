from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import manage, verify
from app.auth.permissions import authorize

from app.routers.alerts import alert_req_schema, alert_res_schema, alert_crud

router = APIRouter()

@router.post(
    "/",
    response_model=alert_res_schema.create_res_model,
    status_code=status.HTTP_201_CREATED,
    # responses=create_admin.responses,
)
async def create_alerts(
    req: alert_req_schema.create_alert,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser(
        user_token,
    )

    data = {
        "timestamp": req.datetime,
        "alert": req.alert
    }
    try:
        await alert_crud.create_alert_data(**data)
        return {"device_id": device_id, "detail": "Alert created"}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
