import os
import pytest
from fastapi import status
from app.auth import manage
from tests.utils import get_token
# import uuid

id_token = get_token.login_and_get_id_token(
    os.getenv("FIREBASE_SUPERUSER_ADMIN_EMAIL"),
    os.getenv("FIREBASE_SUPERUSER_ADMIN_PASSWORD"),
)


# Testing for Create Community user response code is 201
@pytest.mark.asyncio
async def test_create_community_user(test_app_with_db):
    global community_id
    # community_id = uuid.UUID("6201419a-9834-46aa-bde8-62452d6928d9")
    community_id = "27d61e61-f5d3-4252-9383-f2559cb4444b"
    request_body = {
        "name": "fueb",
        "mobile": "+919964489712",
        "title": "treasurer",
        "email": "usha@example.com",
        "password": "string",
        "birth_date": "2024-04-15",
        "role": "admin",
        "user_status": "active",
    }

    # Use the test_app_with_db object as an AsyncClient object
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.post(
        f"/api/community_users/{community_id}",
        json=request_body,
        headers=headers,
    )
    global user_id
    user_id = response.json()["user_id"]
    assert response.status_code == 201


# Testing for Create Community user invalid request response code is 422
@pytest.mark.asyncio
async def test_invalid_create_community_user(test_app_with_db):
    request_body = {
        "name": 12345,
        "mobile": "+99900677312",
        "title": "treasurer",
        "email": "user@example.com",
        "password": "string",
        "birth_date": "2024-04-15",
        "role": "admin",
        "user_status": "active",
    }
    # Use the test_app_with_db object as an AsyncClient object
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.post(
        f"/api/community_users/{community_id}",
        json=request_body,
        headers=headers,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# Testing for Read Community user response code is 200
@pytest.mark.asyncio
async def test_get_one_community_user(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.get(
        f"/api/community_users/{community_id}/{user_id}", # noqa
        headers=headers,
    )
    assert (
        response.status_code == 200
    ), f"Unexpected response: {response.json()}"
    assert response.json()["user_id"] == user_id


# Testing for Read invalid Cmmunity user response code is 404
@pytest.mark.asyncio
async def test_get_404_invalid_community_user(test_app_with_db):
    user = "QdYURPq4vAa7pkrFxLCHZsm0Gh12"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.get(
        f"/api/community_users/{community_id}/{user}", # noqa
        headers=headers,
    )
    assert (
        response.status_code == 404
    ), f"Unexpected response: {response.json()}"


# Testing for Read All Community users response code is 200
@pytest.mark.asyncio
async def test_get_all_community_users(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.get(
        f"/api/community_users/{community_id}",
        headers=headers,
    )
    assert (
        response.status_code == 200
    ), f"Unexpected response: {response.json()}"  # Noqa
    assert len(response.json()) >= 0


# Testing for update Community user response code is 200
@pytest.mark.asyncio
async def test_update_community_user(test_app_with_db):
    request_body = {
        "name": "string",
        "mobile": "+919900677312",
        "title": "manager",
        "email": "user@example.com",
        "birth_date": "2024-04-15",
        "role": "admin",
        "user_status": "active",
    }
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.put(
        f"/api/community_users/{community_id}/{user_id}", # noqa
        json=request_body,
        headers=headers,
    )
    assert (
        response.status_code == 200
    ), f"Unexpected response: {response.json()}"
    assert response.json()["user_id"] == user_id
    assert response.json()["updated_info"] == request_body


# Testing for Update invalid Community user response code is 404
@pytest.mark.asyncio
async def test_404_update_community_user(test_app_with_db):
    user = "QdYURPq4vAa7pkrFxLCHZsm0Gh12"
    request_body = {
        "name": "string",
        "mobile": "+919900990091",
        "title": "manager",
        "email": "user@example.com",
        "birth_date": "2024-04-15",
        "role": "admin",
        "user_status": "active",
    }
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.put(
        f"/api/community_users/{community_id}/{user}", # noqa
        json=request_body,
        headers=headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    # assert response.json["detail"] == "User not found"


# Testing for Update Community user invalid request body response code is 422
@pytest.mark.asyncio
async def test_invalid_422_update_community_user(test_app_with_db):
    request_body = {
        "name": 12345,
        "mobile": "+919900990091",
        "title": "manager",
        "email": "user@example.com",
        "birth_date": "2024-04-15",
        "role": "admin",
        "user_status": "active",
    }
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.put(
        f"/api/community_users/{community_id}/{user_id}",
        json=request_body,
        headers=headers,
    )
    assert (
        response.status_code == 422
    ), f"Unexpected response: {response.json()}"


# Testing for patch Community user response code is 200
@pytest.mark.asyncio
async def test_patch_community_user(test_app_with_db):
    request_body = {
       "mobile": "+919886184486",
       "email": "user@example.com",
       "name": "string",
    }
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.patch(
        f"/api/community_users/{community_id}/{user_id}", # noqa
        json=request_body,
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Unexpected response: {response.json()}"
    assert response.json()["user_id"] == user_id


# Testing for patch invalid Community user response code is 404
@pytest.mark.asyncio
async def test_patch_404_community_user(test_app_with_db):
    user = "QdYURPq4vAa7pkrFxLCHZsm0Gh12"
    request_body = {
        "mobile": "+919900990091",
        "email": "user@example.com",
        "name": "string",
    }
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.patch(
        f"/api/community_users/{community_id}/{user}", # noqa
        json=request_body,
        headers=headers,
    )
    assert (
        response.status_code == 404
    ), f"Unexpected response: {response.json()}"


# Testing for patch Community user invalid request response code is 422
@pytest.mark.asyncio
async def test_patch_422_community_user(test_app_with_db):
    request_body = {
        "mobile": "+919900990091",
        "email": "user@example.com",
        "name": 12345,
    }
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.patch(
        f"/api/community_users/{community_id}/{user_id}", # noqa
        json=request_body,
        headers=headers,
    )
    assert (
        response.status_code == 422
    ), f"Unexpected response: {response.json()}"


# Testing for Delete Community user response code is 204
@pytest.mark.asyncio
async def test_delete_community_user(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.delete(
        f"/api/community_users/{community_id}/{user_id}", # noqa
        headers=headers,
    )
    await manage.delete_user(user_id)
    assert (
        response.status_code == 204
    ), f"Unexpected response: {response.json()}"  # Noqa


# Testing for Delete Community user response code is 204
@pytest.mark.asyncio
async def test_delete_404_community_user(test_app_with_db):
    user = "QdYURPq4vAa7pkrFxLCHZsm0Gh12"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.delete(
        f"/api/community_users/{community_id}/{user}", # noqa
        headers=headers,
    )
    assert (
        response.status_code == 404
    ), f"Unexpected response: {response.json()}"  # Noqa
