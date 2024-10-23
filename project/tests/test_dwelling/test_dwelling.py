import os
import pytest
from fastapi import status

from tests.utils import get_token

id_token = get_token.login_and_get_id_token(
    os.getenv("FIREBASE_SUPERUSER_ADMIN_EMAIL"),
    os.getenv("FIREBASE_SUPERUSER_ADMIN_PASSWORD"),
)


# Testing Create a new dwelling for particular community 201_CREATED
@pytest.mark.asyncio
async def test_create_201_dwelling(test_app_with_db):
    request_body = {
        "block": "A",
        "floor_no": "1st",
        "flat_no": "105",
        "type_of": "2BHK",
    }
    global community_id
    community_id = "27d61e61-f5d3-4252-9383-f2559cb4444b"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.post(
        f"/api/dwelling/community/{community_id}",
        json=request_body,
        headers=headers,
    )
    global dwelling_id
    dwelling_id = response.json()["dwelling_id"]
    assert (
        response.status_code == status.HTTP_201_CREATED
        ), f"Unexpected response: {response.json()}"


# Testing Create a new dwelling for particular community 404_NOT_FOUND
@pytest.mark.asyncio
async def test_create_404_dwelling(test_app_with_db):
    request_body = {
        "block": "A",
        "floor_no": "1st",
        "flat_no": "101",
        "type_of": "3BHK",
    }
    community = "e7381be1-0558-4c24-9f0a-de9af8569fa1"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.post(
        f"/api/dwelling/community/{community}",
        json=request_body,
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), f"Unexpected response: {response.json()}"


# Testing Create a new dwelling for community 422_UNPROCESSABLE_ENTITY
@pytest.mark.asyncio
async def test_create_422_dwelling(test_app_with_db):
    request_body = {
        "block": 1,
        "floor_no": "1st",
        "flat_no": "101",
        "type_of": "3BHK",
    }
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.post(
        f"/api/dwelling/community/{community_id}",
        json=request_body,
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    ), f"Unexpected response: {response.json()}"


# Testing Read a dwelling response code 200_OK
@pytest.mark.asyncio
async def test_read_one_200_dwelling(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.get(
        f"/api/dwelling/{dwelling_id}",
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Unexpected response: {response.json()}"


# Testing Read a dwelling response code 404_NOT_FOUND
@pytest.mark.asyncio
async def test_read_one_404_dwelling(test_app_with_db):
    dwelling = "ed811c0a-bd60-4930-a741-0a9c87273ec3"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.get(
        f"/api/dwelling/{dwelling}",
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), f"Unexpected response: {response.json()}"


# Testing Read all dwelling response code 200_OK
@pytest.mark.asyncio
async def test_read_all_200_dwelling(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.get(
        f"/api/dwelling/community/{community_id}",
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Unexpected response: {response.json()}"


# Testing Read all dwelling response code 404_NOT_FOUND
@pytest.mark.asyncio
async def test_read_all_404_dwelling(test_app_with_db):
    community = "6201419a-9834-46aa-bde8-62452d6928d0"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.get(
        f"/api/dwelling/community/{community}",
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), f"Unexpected response: {response.json()}"


# Testing patch a dwelling response code 200_ok
@pytest.mark.asyncio
async def test_patch_200_dwelling(test_app_with_db):
    request_body = {
        "block": "B",
        "floor_no": "2nd",
        "flat_no": "201",
        "type_of": "2BHK",
    }
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.patch(
        f"/api/dwelling/{dwelling_id}",
        json=request_body,
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Unexpected response: {response.json()}"


# Testing patch a dwelling response code 404_NOT_FOUND
@pytest.mark.asyncio
async def test_patch_404_dwelling(test_app_with_db):
    request_body = {
        "block": "B",
        "floor_no": "2nd",
        "flat_no": "201",
        "type_of": "2BHK",
    }
    dwelling = "ed811c0a-bd60-4930-a741-0a9c87273ec3"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.patch(
        f"/api/dwelling/{dwelling}",
        json=request_body,
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), f"Unexpected response: {response.json()}"


# Testing patch a dwelling response code 422_UNPROCESSABLE_ENTITY
@pytest.mark.asyncio
async def test_patch_422_dwelling(test_app_with_db):
    request_body = {
        "block": 2,
        "floor_no": "2nd",
        "flat_no": "201",
        "type_of": "2BHK",
    }
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.patch(
        f"/api/dwelling/{dwelling_id}",
        json=request_body,
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    ), f"Unexpected response: {response.json()}"


# Testing Delete a dwelling response code 204_NO_CONTENT
@pytest.mark.asyncio
async def test_delete_204_dwelling(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.delete(
        f"/api/dwelling/{dwelling_id}",
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_204_NO_CONTENT
    ), f"Unexpected response: {response.json()}"


# Testing Delete invalid dwelling response code 404_not_found
@pytest.mark.asyncio
async def test_delete_404_dwelling(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.delete(
        f"/api/dwelling/{dwelling_id}",
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), f"Unexpected response: {response.json()}"
