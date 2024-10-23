import os
import pytest
from fastapi import status

from app.auth import manage
from tests.utils import get_token

id_token = get_token.login_and_get_id_token(
    os.getenv("FIREBASE_SUPERUSER_ADMIN_EMAIL"),
    os.getenv("FIREBASE_SUPERUSER_ADMIN_PASSWORD"),
)


# Testing for Create Admin user response code is 201
@pytest.mark.asyncio
async def test_create_admin_user(test_app_with_db):
    request_body = {
        "name": "test_user",
        "employee_id": "0012",
        "mobile": "+917676756323",
        "email": "test_user1@google.com",
        "password": "string",
        "user_status": "active",
        "role": "admin",
    }
    # Use the test_app_with_db object as an AsyncClient object
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.post(
        "/api/admin/",
        json=request_body,
        headers=headers,
    )
    global user_id
    user_id = response.json()["user_id"]

    assert (
        response.status_code == status.HTTP_201_CREATED
    ), f"Unexpected response: {response.json()}"


# Testing for Create Admin user invalid request response code is 422
@pytest.mark.asyncio
async def test_invalid_create_admin_user(test_app_with_db):
    request_body = {
        "name": 123456,
        "employee_id": "string",
        "mobile": "+919108399999",
        "email": "test_user_2@google.com",
        "password": "string_test91",
        "user_status": "active",
        "role": "admin",
    }
    # Use the test_app_with_db object as an AsyncClient object
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.post(
        "/api/admin/",
        json=request_body,
        headers=headers,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# Testing for Read Admin user response code is 200
@pytest.mark.asyncio
async def test_get_one_admin_user(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.get(
        f"/api/admin/{user_id}",
        headers=headers,
    )
    assert (
        response.status_code == 200
    ), f"Unexpected response: {response.json()}"
    assert response.json()["user_id"] == user_id


# Testing for Read invalid Admin user response code is 404
@pytest.mark.asyncio
async def test_get_404_invalid_admin_user(test_app_with_db):
    user = "QdYURPq4vAa7pkrFxLCHZsm0Gh12"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.get(
        f"/api/admin/{user}",
        headers=headers,
    )
    assert (
        response.status_code == 404
    ), f"Unexpected response: {response.json()}"
    # assert response.json["detail"] == "User not found"


# Testing for Read All Admin users response code is 200
@pytest.mark.asyncio
async def test_get_all_admin_users(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.get(
        "/api/admin/",
        headers=headers,
    )
    assert (
        response.status_code == 200
    ), f"Unexpected response: {response.json()}"  # Noqa
    assert len(response.json()) >= 0


# Testing for update Admin user response code is 200
@pytest.mark.asyncio
async def test_update_admin_user(test_app_with_db):
    request_body = {
        "name": "test_user",
        "mobile": "+919108399999",
        "email": "test_user_3@google.com",
        "role": "admin",
    }
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.put(
        f"/api/admin/{user_id}",
        json=request_body,
        headers=headers,
    )
    assert (
        response.status_code == 200
    ), f"Unexpected response: {response.json()}"
    assert response.json()["user_id"] == user_id
    assert response.json()["updated_info"] == request_body


# Testing for Update invalid Admin user response code is 404
@pytest.mark.asyncio
async def test_404_update_admin_user(test_app_with_db):
    user = "QdYURPq4vAa7pkrFxLCHZsm0Gh12"
    request_body = {
        "name": "test_user",
        "mobile": "+919108399999",
        "email": "test_user_3@google.com",
        "role": "admin",
    }
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.put(
        f"/api/admin/{user}",
        json=request_body,
        headers=headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    # assert response.json["detail"] == "User not found"


# Testing for Update Admin user invalid request body response code is 422
@pytest.mark.asyncio
async def test_invalid_422_update_admin_user(test_app_with_db):
    request_body = {
        "name": 12345,
        "mobile": "+919108399999",
        "email": "test_user_3@google.com",
        "role": "admin",
    }
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.put(
        f"/api/admin/{user_id}",
        json=request_body,
        headers=headers,
    )
    assert (
        response.status_code == 422
    ), f"Unexpected response: {response.json()}"


# Testing for patch Admin user response code is 200
@pytest.mark.asyncio
async def test_patch_admin_user(test_app_with_db):
    request_body = {
        "role": "superuser",
    }
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.patch(
        f"/api/admin/{user_id}",
        json=request_body,
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Unexpected response: {response.json()}"
    assert response.json()["user_id"] == user_id
    assert response.json()["detail"] == "user role changed"


# Testing for patch invalid Admin user response code is 404
@pytest.mark.asyncio
async def test_patch_404_admin_user(test_app_with_db):
    user = "QdYURPq4vAa7pkrFxLCHZsm0Gh12"
    request_body = {
        "role": "superuser",
    }
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.patch(
        f"/api/admin/{user}",
        json=request_body,
        headers=headers,
    )
    assert (
        response.status_code == 404
    ), f"Unexpected response: {response.json()}"


# Testing for patch Admin user invalid request response code is 422
@pytest.mark.asyncio
async def test_patch_422_admin_user(test_app_with_db):
    request_body = {
        "role": "super",
    }
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.patch(
        f"/api/admin/{user_id}",
        json=request_body,
        headers=headers,
    )
    assert (
        response.status_code == 422
    ), f"Unexpected response: {response.json()}"


# Testing for Delete Admin user response code is 204
@pytest.mark.asyncio
async def test_delete_admin_user(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.delete(
        f"/api/admin/{user_id}",
        headers=headers,
    )
    await manage.delete_user(user_id)
    assert (
        response.status_code == 204
    ), f"Unexpected response: {response.json()}"  # Noqa


# Testing for Delete Admin user response code is 204
@pytest.mark.asyncio
async def test_delete_404_admin_user(test_app_with_db):
    user = "QdYURPq4vAa7pkrFxLCHZsm0Gh12"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.delete(
        f"/api/admin/{user}",
        headers=headers,
    )
    assert (
        response.status_code == 404
    ), f"Unexpected response: {response.json()}"  # Noqa
