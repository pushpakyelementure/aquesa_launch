import os
import pytest
from fastapi import status

from app.auth import manage
from tests.utils import get_token

id_token = get_token.login_and_get_id_token(
    os.getenv("FIREBASE_SUPERUSER_ADMIN_EMAIL"),
    os.getenv("FIREBASE_SUPERUSER_ADMIN_PASSWORD"),
)


# Create the valid App user 201_CREATED
@pytest.mark.asyncio
async def test_create_valid_app_user_201(test_app_with_db):
    request_body = {
        "name": "pushpa",
        "mobile": "+917576751234",
        "email": "users@example.com",
        "profile_picture": "https://example.com/",
        "birth_date": "1993-08-20",
    }
    global community_id
    community_id = "27d61e61-f5d3-4252-9383-f2559cb4444b"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.post(
        f"/api/app_users/{community_id}",
        json=request_body,
        headers=headers,
    )
    global user_id
    user_id = response.json()["user_id"]
    assert (
        response.status_code == 201
    ), f"Unexpected response: {response.json()}"  # Noqa
    assert response.json()["detail"] == "app user created"


# Create the valid App user 404 NOT found error
@pytest.mark.asyncio
async def test_create_404_invalid_app_user(test_app_with_db):
    request_body = {
        "name": "nishu",
        "mobile": "+917353953229",
        "email": "user@example.com",
        "profile_picture": "https://example.com/",
        "birth_date": "1993-08-20",
    }
    community = "ee80c7a0-fe6e-465b-b003-c7886ee31fc8"
    response = await test_app_with_db.post(
        f"/api/app_users/{community}",
        json=request_body,
        headers={"Authorization": f"Bearer {id_token}"},
    )

    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    )


# Create the valid App user 422_UNPROCESSABLE_ENTITY
@pytest.mark.asyncio
async def test_create_422_invalid_app_user(test_app_with_db):
    request_body = {
        "name": 12345,
        "mobile": "+917353953229",
        "email": "user@example.com",
        "profile_picture": "user/bin/image.jpg",
        "birth_date": "1993-08-20",
    }
    response = await test_app_with_db.post(
        f"/api/app_users/{community_id}",
        json=request_body,
        headers={"Authorization": f"Bearer {id_token}"},
    )
    # Assertions
    assert (
        response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    ), f"Unexpected response: {response.json()}"  # Noqa


# Read the valid App_user 200_OK
@pytest.mark.asyncio
async def test_read_valid_app_user_200(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.get(
        f"/api/app_users/{community_id}/{user_id}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "pushpa"


# Read invalid App_user status_code 404_NOT_FOUND
@pytest.mark.asyncio
async def test_read_invalid_App_user_404(test_app_with_db):
    community = "92ef02f5-e68e-47fc-a5eb-ad1f9e68ef9e"
    user = "ZeQSE3iJipSgTHr7MjGDD3WFQn74"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.get(
        f"/api/app_users/{community}/{user}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


# ReadAll valid App_user 200_OK
@pytest.mark.asyncio
async def test_readall_valid_app_user_200(test_app_with_db):
    # community = "ee80c7a0-fe6e-465b-b003-c7886ee31fc7"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.get(
        f"/api/app_users/{community_id}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK


# Update the valid app_user 200_OK
@pytest.mark.asyncio
async def test_update_valid_app_user_200(test_app_with_db):
    request_body = {
        "name": "string",
        "mobile": "+911234567899",
        "email": "user@example.com",
        "birth_date": "1993-08-20",
    }
    response = await test_app_with_db.put(
        f"/api/app_users/{community_id}/{user_id}",
        json=request_body,
        headers={"Authorization": f"Bearer {id_token}"},
    )

    # Assertions
    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Unexpected response: {response.json()}"  # Noqa


# Update the valid app_user 404_NotFound
@pytest.mark.asyncio
async def test_update_invalid_app_user_404(test_app_with_db):
    request_body = {
        "name": "string",
        "mobile": "+917676756321",
        "email": "user@example.com",
        "birth_date": "1993-08-20",
    }
    community = "0ceaf43f-ef2b-43f7-b2bf-67c21397f9b7"
    user = "ZeQSE3iJipSgTHr7MjGDD3WFQn74"
    response = await test_app_with_db.put(
        f"/api/app_users/{community}/{user}",
        json=request_body,
        headers={"Authorization": f"Bearer {id_token}"},
    )

    # Assertions
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    )
    # , f"Unexpected response: {response.json()}"  # Noqa


# Update the valid app_user 422_UNPROCESSABLE_ENTITY
@pytest.mark.asyncio
async def test_update_invalid_app_user_422(test_app_with_db):
    request_body = {
        "name": 123456,
        "mobile": "+917353953229",
        "email": "user@example.com",
        "birth_date": "1993-08-20",
    }
    response = await test_app_with_db.put(
        f"/api/app_users/{community_id}/{user_id}",
        json=request_body,
        headers={"Authorization": f"Bearer {id_token}"},
    )

    # Assertions
    assert (
        response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    ), f"Unexpected response: {response.json()}"  # Noqa


# Delete the valid App_user 204
@pytest.mark.asyncio
async def test_delete_valid_app_user_204(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.delete(
        f"/api/app_users/{community_id}/{user_id}",
        headers=headers,
    )
    await manage.delete_user(user_id)
    assert response.status_code == status.HTTP_204_NO_CONTENT


# Delete the valid App_user 204
@pytest.mark.asyncio
async def test_delete_invalid_app_user_404(test_app_with_db):
    user = "ZeQSE3iJipSgTHr7MjGDD3WFQn74"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.delete(
        f"/api/app_users/{community_id}/{user}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
