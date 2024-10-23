import os
import pytest
from fastapi import status

# from app.auth import manage
from tests.utils import get_token

id_token = get_token.login_and_get_id_token(
    os.getenv("FIREBASE_SUPERUSER_ADMIN_EMAIL"),
    os.getenv("FIREBASE_SUPERUSER_ADMIN_PASSWORD"),
)


# Testing Create a Community response code 201
@pytest.mark.asyncio
async def test_create_201_community(test_app_with_db):
    request_body = {
        "community_name": "string2",
        "location": {
            "address": "string",
            "city": "string",
            "state": "string",
            "country": "string",
            "zip_code": "string",
            "time_zone": "string",
        },
        "dwelling_types": [{}],
        "bill_model": "string",
        "billing_cycle_date": 0,
        "billing_start_date": "2024-04-16T05:16:27.615Z",
        "next_invoice_date": "2024-04-16T05:16:27.615Z",
        "gst_no": "string",
        "subscription_status": "active",
    }
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.post(
        "/api/community/",
        json=request_body,
        headers=headers,
    )
    global community_id
    community_id = response.json()["community_id"]
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["community_id"] == community_id


# Testing Create a Community 422_UNPROCESSABLE_ENTITY
@pytest.mark.asyncio
async def test_create_422_community(test_app_with_db):
    request_body = {
        "community_name": "string",
        "location": {
            "address": "string",
            "city": "string",
            "state": "string",
            "country": "string",
            "zip_code": "string",
            "time_zone": "string",
        },
        "dwelling_types": [{}],
        "bill_model": 123456,
        "billing_cycle_date": 0,
        "billing_start_date": "2024-04-16T05:16:27.615Z",
        "next_invoice_date": "2024-04-16T05:16:27.615Z",
        "gst_no": "string",
        "subscription_status": "active",
    }
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.post(
        "/api/community/",
        json=request_body,
        headers=headers,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# Testing Read one community response code 200_OK
@pytest.mark.asyncio
async def test_read_one_200_community(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.get(
        f"/api/community/{community_id}",
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Unexpected response: {response.json()}"


# Testing Read invalid community response code 404_NOT_FOUND
@pytest.mark.asyncio
async def test_read_one_404_community(test_app_with_db):
    community_id = "6201419a-9834-46aa-bde8-62452d6928d0"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.get(
        f"/api/community/{community_id}",
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), f"Unexpected response: {response.json()}"


# Testing Read all community response code 200_OK
@pytest.mark.asyncio
async def test_read_all_200_community(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.get(
        "/api/community/",
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Unexpected response: {response.json()}"


# Testing update a Community response code 200
@pytest.mark.asyncio
async def test_update_200_community(test_app_with_db):
    request_body = {
        "community_name": "str",
        "location": {
            "address": "string",
            "city": "string",
            "state": "string",
            "country": "string",
            "zip_code": "string",
            "time_zone": "string",
        },
        "dwelling_types": [{}],
        "bill_model": "string",
        "billing_cycle_date": 0,
        "billing_start_date": "2024-04-16T05:52:50.610Z",
        "next_invoice_date": "2024-04-16T05:52:50.610Z",
        "gst_no": "string",
        "subscription_status": "active",
    }
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.put(
        f"/api/community/{community_id}",
        json=request_body,
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Unexpected response: {response.json()}"


# Testing update invalid Community response code 404
@pytest.mark.asyncio
async def test_update_404_community(test_app_with_db):
    request_body = {
        "community_name": "string",
        "location": {
            "address": "string",
            "city": "string",
            "state": "string",
            "country": "string",
            "zip_code": "string",
            "time_zone": "string",
        },
        "dwelling_types": [{}],
        "bill_model": "string",
        "billing_cycle_date": 0,
        "billing_start_date": "2024-04-16T05:52:50.610Z",
        "next_invoice_date": "2024-04-16T05:52:50.610Z",
        "gst_no": "string",
        "subscription_status": "active",
    }
    community = "6201419a-9834-46aa-bde8-62452d6928d0"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.put(
        f"/api/community/{community}",
        json=request_body,
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), f"Unexpected response: {response.json()}"


# Testing update invalid Community response code 422
@pytest.mark.asyncio
async def test_update_422_community(test_app_with_db):
    request_body = {
        "community_name": "string",
        "location": {
            "address": "string",
            "city": "string",
            "state": "string",
            "country": "string",
            "zip_code": "string",
            "time_zone": "string",
        },
        "dwelling_types": [{}],
        "bill_model": 123,
        "billing_cycle_date": 0,
        "billing_start_date": "2024-04-16T05:52:50.610Z",
        "next_invoice_date": "2024-04-16T05:52:50.610Z",
        "gst_no": "string",
        "subscription_status": "active",
    }
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.put(
        f"/api/community/{community_id}",
        json=request_body,
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    ), f"Unexpected response: {response.json()}"


# Testing patch a Community response code 200
@pytest.mark.asyncio
async def test_patch_200_community(test_app_with_db):
    request_body = {
        "subscription_status": "active"
        }

    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.patch(
        f"/api/community/{community_id}",
        json=request_body,
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Unexpected response: {response.json()}"


# Testing patch invalid Community response code 404
@pytest.mark.asyncio
async def test_patch_404_community(test_app_with_db):
    request_body = {
        "subscription_status": "active"
        }
    community = "6201419a-9834-46aa-bde8-62452d6928d0"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.patch(
        f"/api/community/{community}",
        json=request_body,
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), f"Unexpected response: {response.json()}"


# Testing patch invalid Community response code 422
@pytest.mark.asyncio
async def test_patch_422_community(test_app_with_db):
    request_body = {
        "subscription_status": "act"
        }
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.patch(
        f"/api/community/{community_id}",
        json=request_body,
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    ), f"Unexpected response: {response.json()}"


# Testing delete a Community response code 204
@pytest.mark.asyncio
async def test_delete_204_community(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.delete(
        f"/api/community/{community_id}",
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_204_NO_CONTENT
    ), f"Unexpected response: {response.json()}"


# Testing delete invalid Community response code 404
@pytest.mark.asyncio
async def test_delete_404_community(test_app_with_db):
    community = "6201419a-9834-46aa-bde8-62452d6928d0"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.delete(
        f"/api/community/{community}",
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), f"Unexpected response: {response.json()}"
