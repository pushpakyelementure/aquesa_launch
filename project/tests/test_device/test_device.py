import os
import pytest
from fastapi import status

from tests.utils import get_token

id_token = get_token.login_and_get_id_token(
    os.getenv("FIREBASE_SUPERUSER_ADMIN_EMAIL"),
    os.getenv("FIREBASE_SUPERUSER_ADMIN_PASSWORD"),
)


# Testing create a new device for specific dwelling response code 201_CREATED.  # noqa
@pytest.mark.asyncio
async def test_create_201_device(test_app_with_db):
    request_body = {
        "device_id": "7901f953-2bb4-4a90-9a72-c54106fda61e",
        "device_type": "water_measure_mechanical",
        "serial_no": "1010",
        "group": "string",
        "tag": "vave1",
        "customTag": ["kitchen"],
        "status": "active",
    }
    global device_id
    # global dwelling_id
    device_id = "7901f953-2bb4-4a90-9a72-c54106fda61e"
    dwelling_id = "7c1f5da0-bbbe-4625-983d-a08176a09993"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.post(
        "/api/device/",
        json=request_body,
        params={"dwelling_id": dwelling_id},
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_201_CREATED
    )
    # , f"Unexpected response: {response.json()}"


# Testing create a new device for invalid dwelling response code 404_NOT_FOUND # noqa
@pytest.mark.asyncio
async def test_create_404_device(test_app_with_db):
    request_body = {
        "device_id": "962f129a-abed-44d2-9987-e31f1c79f28a",
        "device_type": "water_measure_mechanical",
        "serial_no": "1010",
        "group": "string",
        "tag": "vave1",
        "customTag": ["kitchen"],
        "status": "active",
    }
    dwelling = "962f129a-abed-44d2-9987-e31f1c79f27c"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.post(
        "/api/device/",
        json=request_body,
        params={"dwelling_id": dwelling},
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), f"Unexpected response: {response.json()}"


# Testing create a new device for dwelling response code 422 # noqa
@pytest.mark.asyncio
async def test_create_422_device(test_app_with_db):
    request_body = {
        "device_id": "962f129a-abed-44d2-9987-e31f1c7",
        "device_type": "water_measure_mechanical",
        "serial_no": "1010",
        "group": "string",
        "tag": "vave1",
        "customTag": ["kitchen"],
        "status": "active",
    }
    dwelling_id = "7c1f5da0-bbbe-4625-983d-a08176a09993"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.post(
        "/api/device/",
        json=request_body,
        params={"dwelling_id": dwelling_id},
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    ), f"Unexpected response: {response.json()}"


# Testing Read a device response code 200_OK  # noqa
@pytest.mark.asyncio
async def test_read_200_device(test_app_with_db):
    dwelling_id = "7c1f5da0-bbbe-4625-983d-a08176a09993"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.get(
        f"/api/device/dwell/{dwelling_id}",
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Unexpected response: {response.json()}"


# Testing Read a device response code 404_NOT_FOUND  # noqa
@pytest.mark.asyncio
async def test_read_404_device(test_app_with_db):
    dwelling = "962f129a-abed-44d2-9987-e31f1c79f27e"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.get(
        f"/api/device/dwell/{dwelling}",
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), f"Unexpected response: {response.json()}"


# Testing update a device details response code 200_OK.  # noqa
@pytest.mark.asyncio
async def test_update_200_device(test_app_with_db):
    request_body = {
        "device_type": "water_measure_mechanical",
        "serial_no": "1010",
        "group": "string",
        "tag": "vave1",
        "customTag": ["kitchen"],
        "status": "active",
    }
    dwelling_id = "7c1f5da0-bbbe-4625-983d-a08176a09993"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.put(
        f"/api/device/{dwelling_id}/{device_id}",
        json=request_body,
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Unexpected response: {response.json()}"


# Testing update invalid device details response code 404.  # noqa
@pytest.mark.asyncio
async def test_update_404_device(test_app_with_db):
    request_body = {
        "device_type": "water_measure_mechanical",
        "serial_no": "1010",
        "group": "string",
        "tag": "vave1",
        "customTag": ["kitchen"],
        "status": "active",
    }
    dwelling_id = "7c1f5da0-bbbe-4625-983d-a08176a09993"
    device_id = "962f129a-abed-44d2-9987-e31f1c79f280"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.put(
        f"/api/device/{dwelling_id}/{device_id}",
        json=request_body,
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), f"Unexpected response: {response.json()}"


# Testing update invalid device details response code 422_UNPROCESSABLE_ENTITY # noqa
@pytest.mark.asyncio
async def test_update_422_device(test_app_with_db):
    request_body = {
        "device_type": "water_measure_mechanical",
        "serial_no": 1001,
        "group": "string",
        "tag": "vave1",
        "customTag": ["kitchen"],
        "status": "active",
    }
    dwelling_id = "7c1f5da0-bbbe-4625-983d-a08176a09993"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.put(
        f"/api/device/{dwelling_id}/{device_id}",
        json=request_body,
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    ), f"Unexpected response: {response.json()}"


# Testing Delete a device response code 204_NO_CONTENT
@pytest.mark.asyncio
async def test_delete_204_device(test_app_with_db):
    dwelling_id = "7c1f5da0-bbbe-4625-983d-a08176a09993"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.delete(
        f"/api/device/{dwelling_id}/{device_id}",
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_204_NO_CONTENT
    ), f"Unexpected response: {response.json()}"


# Testing Delete invalid device response code 404_NOT_FOUND
@pytest.mark.asyncio
async def test_delete_404_device(test_app_with_db):
    dwelling_id = "7c1f5da0-bbbe-4625-983d-a08176a09993"
    device = "962f129a-abed-44d2-9987-e31f1c79f28b"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.delete(
        f"/api/device/{dwelling_id}/{device}",
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), f"Unexpected response: {response.json()}"
