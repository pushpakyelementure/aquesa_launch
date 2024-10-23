from fastapi import HTTPException, status
from datetime import datetime

from app.db.models.dwelling import device_list, dwelling_model
from app.db.models.valve_status import valve_status_enum, device_status

# from pydantic import UUID
# import uuid


async def create_device(dwelling_id, user_token, **data):
    dwell = await dwelling_model.find_one(
        dwelling_model.dwelling_id == dwelling_id
    )  # noqa
    if dwell is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dwelling not found",
        )
    dwell.devices = dwell.devices or []
    # device_ids = [device.device_id for device in dwell.devices]

    for device in dwell.devices:
        print(data["device_id"])
        print(device)
        if device.device_id == data.get("device_id"):
            print(data["device_id"])
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="device already exists",
            )

    new_device = device_list(**data)
    dwell.devices = dwell.devices or []
    dwell.devices.append(new_device)
    # valve status
    activity_info = {
                  "timestamp": datetime.now(),
                  "action_by": user_token["uid"]
                 }
    valve_status = {
        "device_id": new_device.device_id,
        "valve_status": valve_status_enum.close,
        "tag": "valv01",
        "custom_tag": "kitchen",
        "activity": activity_info
    }
    data_to_db = device_status(**valve_status)

    await dwell.save()
    await data_to_db.insert()
    return dwell


async def get_all_devices_of_dwelling(dwelling_id):
    dwell = await dwelling_model.find_one(
        dwelling_model.dwelling_id == dwelling_id,
    )  # noqa

    if dwell is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dwelling not found",
        )

    return dwell.devices


async def change_device_info(dwelling_id, device_id, **data):
    dwell = await dwelling_model.find_one(
        dwelling_model.dwelling_id == dwelling_id,
    )
    if dwell is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dwelling not found",
        )
    device_to_update = next(
        (dev for dev in (dwell.devices or []) if dev.device_id == device_id),
        None,
    )
    if device_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found",
        )
    # Update the specified fields in the device
    for key, value in data.items():
        if value is not None:
            setattr(device_to_update, key, value)

    # Save the updated dwelling document
    await dwell.save()
    return dwell


async def delete_device(dwelling_id, device_id):
    dwell = await dwelling_model.find_one(
        dwelling_model.dwelling_id == dwelling_id,
    )
    if dwell is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dwelling not found",
        )
    device_to_delete = next(
        (dev for dev in (dwell.devices or []) if dev.device_id == device_id),
        None,
    )
    if device_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found",
        )

    dwell.devices.remove(device_to_delete)

    await dwell.save()
    return None
