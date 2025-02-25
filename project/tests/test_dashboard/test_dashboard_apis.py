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

# Testing for one community all infomation  response code is 200
@pytest.mark.asyncio
async def test_get_info_community(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    community_id = "9d12da45-8a93-45b1-976c-1bfc4ea27c08"
    response = await test_app_with_db.get(
        f"api/dashboard/{community_id}",  # noqa
        headers=headers,
    )

    assert response.status_code == 200, f"Unexpected response: {response.json()}"  # noqa


# Testing for one community all infomation  response code is 404
@pytest.mark.asyncio
async def test_get_info_community_404(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    community_id = "9d12da45-8a93-45b1-976c-1bfc4ea27c08"
    response = await test_app_with_db.get(
        f"api/dashboard/csm/{community_id}",  # url is incorrect
        headers=headers,
    )

    assert response.status_code == 404, f"Unexpected response: {response.json()}"  # noqa


# Testing for one community all infomation  response code is 422
@pytest.mark.asyncio
async def test_get_info_community_422(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    community_id = "string" # community_id is not a string its UUID4
    response = await test_app_with_db.get(
        f"api/dashboard/{community_id}",
        headers=headers,
    )

    assert response.status_code == 422, f"Unexpected response: {response.json()}"  # noqa


# Testing for Read block wise csm of Community response code is 200
@pytest.mark.asyncio
async def test_get_block_wise_data(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    community_id = "9d12da45-8a93-45b1-976c-1bfc4ea27c08"

    params = {
        "start_date": "2025-02-21 00:00:00",
        "end_date": "2025-02-21 23:59:59",
    }

    response = await test_app_with_db.get(
        f"api/dashboard/tower/{community_id}",  # noqa
        headers=headers,
        params=params,
    )

    assert response.status_code == 200, f"Unexpected response: {response.json()}"  # noqa


# # Testing for Read block wise csm of Community response code is 404
@pytest.mark.asyncio
async def test_get_block_wise_data_404(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    community_id = "7c1f5da0-bbbe-4625-983d-a08176a09993"

    params = {
        "start_date": "2025-02-21 00:00:00",
        "end_date": "2025-02-21 23:59:59",
    }

    response = await test_app_with_db.get(
        f"api/dashboard/tower/{community_id}",  # noqa
        headers=headers,
        params=params,
    )

    assert response.status_code == 404, f"Unexpected response: {response.json()}"  # noqa


# Testing for Read block wise csm of Community response code is 422
@pytest.mark.asyncio
async def test_get_block_wise_data_422(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    community_id = "9d12da45-8a93-45b1-976c-1bfc4ea27c08",

    params = {
        "start_date": "2025-02-21 00:00:00",
        "end_date": "20-02-2025 23:59:59", # date formate  is wrong 
    }

    response = await test_app_with_db.get(
        f"api/dashboard/tower/{community_id}",
        headers=headers,
        params=params,
    )

    assert response.status_code == 422, f"Unexpected response: {response.json()}"  # noqa


# Testing for Community water usage info response code is 200
@pytest.mark.asyncio
async def test_get_water_usage(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    community_id = "9d12da45-8a93-45b1-976c-1bfc4ea27c08"
    params = {
        "start_date": "2025-02-21 00:00:00",
        "end_date": "2025-02-21 23:59:59",
        "aggregation": "day",
    }
    
    response = await test_app_with_db.get(
        f"api/dashboard/water_usage/{community_id}",  # noqa
        headers=headers,
        params=params,
    )

    assert response.status_code == 200, f"Unexpected response: {response.json()}"  # noqa


# Testing for Community water usage info response code is 422
@pytest.mark.asyncio
async def test_get_water_usage_422(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    params = {
        "start_date": "2025-02-21 00:00:00",
        "end_date": "2025-02-21 23:59:59",
        "aggregation": "year", # year is not in enum
    }
    community_id = "9d12da45-8a93-45b1-976c-1bfc4ea27c08",
    response = await test_app_with_db.get(
        f"api/dashboard/water_usage/{community_id}",  # noqa
        headers=headers,
        params=params,
    )

    assert response.status_code == 422, f"Unexpected response: {response.json()}"  # noqa


# Testing for Community water usage info response code is 404
@pytest.mark.asyncio
async def test_get_water_usage_404(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    community_id = "7c1f5da0-bbbe-4625-983d-a08176a09993"
    params = {
        "start_date": "2025-02-21 00:00:00",
        "end_date": "2025-02-21 23:59:59",
        "aggregation": "day",
    }
    response = await test_app_with_db.get(
        f"api/dashboard/water_usage/{community_id}",
        headers=headers,
        params=params,
    )

    assert response.status_code == 404, f"Unexpected response: {response.json()}"  # noqa