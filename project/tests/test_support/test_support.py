import os
import pytest
from fastapi import status
from app.auth import manage
from tests.utils import get_token


id_token = get_token.login_and_get_id_token(
    os.getenv("FIREBASE_SUPERUSER_ADMIN_EMAIL"),
    os.getenv("FIREBASE_SUPERUSER_ADMIN_PASSWORD"),
)


# Testing for get all tickets using community_id response code is 200
@pytest.mark.asyncio
async def test_get_all_tickets(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    community_id = "40843a39-13e6-4137-a0ec-da82a1a02be8"

    response = await test_app_with_db.get(
        f"/api/support/support/{community_id}",  # noqa
        headers=headers,
    )

    assert response.status_code == 200, f"Unexpected response: {response.json()}"  # noqa


# Testing for get all tickets using community_id response code is 404
@pytest.mark.asyncio
async def test_get_all_tickets_404(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    community_id = "40843a39-13e6-4137-a0ec-da82a1a02be9"

    response = await test_app_with_db.get(
        f"/api/support/support/{community_id}",  # noqa
        headers=headers,
    )

    assert response.status_code == 404, f"Unexpected response: {response.json()}"  # noqa


# Testing for get ticket using sr_id response code is 200
@pytest.mark.asyncio
async def test_get_ticket_sr_id(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    sr_id = "01"

    response = await test_app_with_db.get(
        f"/api/support/{sr_id}",  # noqa
        headers=headers,
    )

    assert response.status_code == 200, f"Unexpected response: {response.json()}"  # noqa


# Testing for get ticket using sr_id response code is 404
@pytest.mark.asyncio
async def test_get_ticket_sr_id_404(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    sr_id = "03"

    response = await test_app_with_db.get(
        f"/api/support/{sr_id}",  # noqa
        headers=headers,
    )

    assert response.status_code == 404, f"Unexpected response: {response.json()}"  # noqa


# Testing for get ticket using dwelling_id response code is 200
@pytest.mark.asyncio
async def test_get_ticket_dwelling_id(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    dwelling_id = "b451f328-1577-4231-865b-e2da030bffab"

    response = await test_app_with_db.get(
        f"/api/support/dwelling/{dwelling_id}",  # noqa
        headers=headers,
    )

    assert response.status_code == 200, f"Unexpected response: {response.json()}"  # noqa


# Testing for get ticket using dwelling_id response code is 404
@pytest.mark.asyncio
async def test_get_ticket_dwelling_id_404(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    dwelling_id = "b451f328-1577-4231-865b-e2da030bffab"

    response = await test_app_with_db.get(
        f"/api/support/dwelling/{dwelling_id}",  # noqa
        headers=headers,
    )

    assert response.status_code == 200, f"Unexpected response: {response.json()}"  # noqa


# Testing Create a ticket using community_id and dwelling_id response code is 201
@pytest.mark.asyncio
async def test_create_ticket_dwelling(test_app_with_db):
    community_id = "27d61e61-f5d3-4252-9383-f2559cb4444b"
    dwelling_id = "7c1f5da0-bbbe-4625-983d-a08176a09993"

    request_body = {
        "sr_id": "02",
        "community_id": community_id,
        "dwelling_id": dwelling_id,
        "date": "2025-02-26T07:14:01.569Z",
        "category": "web_app_issues",
        "description": "string",
        "status": "New",
        "documents": ["https://example.com/"],
        "timeline": [
            {
                "name": "string",
                "date": "2025-02-26T07:14:01.569Z",
                "description": "string",
                "document": ["https://example.com/"],
            }
        ],
    }
    print(request_body)
    headers = {"Authorization": f"Bearer {id_token}"}
    
    response = await test_app_with_db.post(
        f"/api/support/{community_id}/{dwelling_id}",
        json=request_body,
        headers=headers,
    )
    assert response.status_code == status.HTTP_201_CREATED, f"Unexpected response: {response.json()}"  # noqa


# Testing Create a ticket using community_id and dwelling_id response code is 404
@pytest.mark.asyncio
async def test_create_ticket_dwelling_404(test_app_with_db):
    community_id = "27d61e61-f5d3-4252-9383-f2559cb4444c"
    dwelling_id = "7c1f5da0-bbbe-4625-983d-a08176a09993"

    request_body = {
        "sr_id": "02",
        "community_id": community_id,
        "dwelling_id": dwelling_id,
        "date": "2025-02-26T07:14:01.569Z",
        "category": "web_app_issues",
        "description": "string",
        "status": "New",
        "documents": ["https://example.com/"],
        "timeline": [
            {
                "name": "string",
                "date": "2025-02-26T07:14:01.569Z",
                "description": "string",
                "document": ["https://example.com/"],
            }
        ],
    }
    print(request_body)
    headers = {"Authorization": f"Bearer {id_token}"}
    
    response = await test_app_with_db.post(
        f"/api/support/{community_id}/{dwelling_id}",
        json=request_body,
        headers=headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND, f"Unexpected response: {response.json()}"  # noqa


# Testing Create a ticket using community_id and dwelling_id response code is 422
@pytest.mark.asyncio
async def test_create_ticket_dwelling_422(test_app_with_db):
    community_id = "27d61e61-f5d3-4252-9383-f2559cb4444b"
    dwelling_id = "7c1f5da0-bbbe-4625-983d-a08176a09993"

    request_body = {
        "sr_id": 11, # its a string, not an integer 
        "community_id": community_id,
        "dwelling_id": dwelling_id,
        "date": "2025-02-26T07:14:01.569Z",
        "category": "web_app_issues",
        "description": "string",
        "status": "New",
        "documents": ["https://example.com/"],
        "timeline": [
            {
                "name": "string",
                "date": "2025-02-26T07:14:01.569Z",
                "description": "string",
                "document": ["https://example.com/"],
            }
        ],
    }
    print(request_body)
    headers = {"Authorization": f"Bearer {id_token}"}
    
    response = await test_app_with_db.post(
        f"/api/support/{community_id}/{dwelling_id}",
        json=request_body,
        headers=headers,
    )
    assert response.status_code == 422, f"Unexpected response: {response.json()}"  # noqa