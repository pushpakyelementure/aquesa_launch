from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4

from app.auth import verify
from app.auth.permissions import authorize
from app.routers.devices import device_crud, device_req_schema, device_res_schema # noqa
from app.routers.devices.device_res_docs import (
    create_device,
    delete_device,
    read_device,
    update_device,
)

router = APIRouter()


# Read all specific dwelling devices using GET method
@router.get(
    "/dwell/{dwelling_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[device_res_schema.devices],
    responses=read_device.responses,
)
async def get_all_devices_of_dwelling(
    dwelling_id: UUID4, user_token=Depends(verify.get_user_token)
):
    await authorize.user_is_superuser_or_admin_or_support_or_field(
        user_token=user_token,
    )
    try:
        devices = await device_crud.get_all_devices_of_dwelling(dwelling_id)
        return [
            {
                "device_id": device.device_id,
                "device_type": device.device_type,
                "serial_no": device.serial_no,
                "group": device.group,
                "tag": device.tag,
                "customTag": device.customTag,
                "status": device.status,
            }
            for device in devices
        ]
    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Create a new Device information POST method
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=device_res_schema.create_device,
    responses=create_device.responses,
)
async def add_device(
    dwelling_id: UUID4,
    req: device_res_schema.devices,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser_or_admin_or_support_or_field(
        user_token=user_token,
    )
    data_to_db = {
        "device_id": req.device_id,
        "device_type": req.device_type,
        "serial_no": req.serial_no,
        "group": req.group,
        "tag": req.tag,
        "customTag": req.customTag,
        "status": req.status,
    }

    try:
        await device_crud.create_device(dwelling_id, user_token, **data_to_db)  # noqa
        return {
            "detail": "Device Added Successfully",
        }
    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Update the device information using PUT method
@router.put(
    "/{dwelling_id}/{device_id}",
    status_code=status.HTTP_200_OK,
    response_model=device_res_schema.update_device,
    responses=update_device.responses,
)
async def change_device_info(
    dwelling_id: UUID4,
    device_id: UUID4,
    req: device_req_schema.devices,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser_or_admin_or_support_or_field(
        user_token=user_token,
    )
    data = {
        "device_type": req.device_type,
        "serial_no": req.serial_no,
        "group": req.group,
        "tag": req.tag,
        "customTag": req.customTag,
        "status": req.status,
    }
    try:
        await device_crud.change_device_info(dwelling_id, device_id, **data)
        return {
            "detail": "Device Updated Successfully",
        }
    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Delete a device information using DELETE method
@router.delete(
    "/{dwelling_id}/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=delete_device.responses,
)
async def delete_device(
    dwelling_id: UUID4, device_id: UUID4, user_token=Depends(verify.get_user_token) # noqa
):
    await authorize.user_is_superuser_or_admin_or_support_or_field(
        user_token=user_token,
    )
    try:
        await device_crud.delete_device(dwelling_id, device_id)
        return None
    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
