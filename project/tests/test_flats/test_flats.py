import os
import pytest
from fastapi import status
from app.auth import manage
from tests.utils import get_token


id_token = get_token.login_and_get_id_token(
    os.getenv("FIREBASE_SUPERUSER_ADMIN_EMAIL"),
    os.getenv("FIREBASE_SUPERUSER_ADMIN_PASSWORD"),
)


# Testing for get flats details using dwelling_id response code is 200
@pytest.mark.asyncio
async def test_get_flats_details(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    dwelling_id = "7c1f5da0-bbbe-4625-983d-a08176a09993"

    response = await test_app_with_db.get(
        f"/api/flats/{dwelling_id}",
        headers=headers,
    )

    assert response.status_code == 200, f"Unexpected response: {response.json()}"  # noqa


# Testing for get flats details using dwelling_id response code is 404
@pytest.mark.asyncio
async def test_get_flats_details_404(test_app_with_db):
    headers = {"Authorization": f"Bearer {id_token}"}
    dwelling_id = "7c1f5da0-bbbe-4625-983d-a08176a09994"

    response = await test_app_with_db.get(
        f"/api/flats/{dwelling_id}",
        headers=headers,
    )

    assert response.status_code == 404, f"Unexpected response: {response.json()}"  # noqa


# Testing change ownership by dwelling_id response code is 201
@pytest.mark.asyncio
async def test_change_ownership_by_dwelling(test_app_with_db):
    dwelling_id = "7c1f5da0-bbbe-4625-983d-a08176a09993"

    request_body = {
            "name": "pushpa",
            "mobile": "+917676756311",
            "email": "user@example.com"
        }
    
    headers = {"Authorization": f"Bearer {id_token}"}
    
    response = await test_app_with_db.post(
        f"/api/flats/{dwelling_id}/owner",
        json=request_body,
        headers=headers,
    )
    assert response.status_code == 201, f"Unexpected response: {response.json()}"  # noqa


# Testing change ownership by dwelling_id response code is 404
@pytest.mark.asyncio
async def test_change_ownership_by_dwelling_404(test_app_with_db):
    dwelling_id = "7c1f5da0-bbbe-4625-983d-a08176a09994"

    request_body = {
            "name": "pushpa",
            "mobile": "+917676756311",
            "email": "user@example.com"
        }
    
    headers = {"Authorization": f"Bearer {id_token}"}
    
    response = await test_app_with_db.post(
        f"/api/flats/{dwelling_id}/owner",
        json=request_body,
        headers=headers,
    )
    assert response.status_code == 404, f"Unexpected response: {response.json()}"  # noqa

# Testing change ownership by dwelling_id response code is 422
@pytest.mark.asyncio
async def test_change_ownership_by_dwelling_422(test_app_with_db):
    dwelling_id = "7c1f5da0-bbbe-4625-983d-a08176a09993"

    request_body = {
            "name": "pushpa",
            "mobile": "+917676756311",
            "email": "pushpa@gmail"
        }
    
    headers = {"Authorization": f"Bearer {id_token}"}
    
    response = await test_app_with_db.post(
        f"/api/flats/{dwelling_id}/owner",
        json=request_body,
        headers=headers,
    )
    assert response.status_code == 422, f"Unexpected response: {response.json()}"  # noqa


# Testing Add tenant by dwelling_id response code is 201
@pytest.mark.asyncio
async def test_add_tenant_by_dwelling(test_app_with_db):
    dwelling_id = "7c1f5da0-bbbe-4625-983d-a08176a09993"

    request_body = {
            "name": "pushpaky",
            "mobile": "+917676756312",
            "email": "user@example.com"
        }
    
    headers = {"Authorization": f"Bearer {id_token}"}
    
    response = await test_app_with_db.post(
        f"/api/flats/{dwelling_id}/",
        json=request_body,
        headers=headers,
    )
    assert response.status_code == 201, f"Unexpected response: {response.json()}"  # noqa


# Testing Add tenant by dwelling_id response code is 404
@pytest.mark.asyncio
async def test_add_tenant_by_dwelling_404(test_app_with_db):
    dwelling_id = "7c1f5da0-bbbe-4625-983d-a08176a09994"

    request_body = {
            "name": "pushpa",
            "mobile": "+917676756311",
            "email": "user@example.com"
        }
    
    headers = {"Authorization": f"Bearer {id_token}"}
    
    response = await test_app_with_db.post(
        f"/api/flats/{dwelling_id}/",
        json=request_body,
        headers=headers,
    )
    assert response.status_code == 404, f"Unexpected response: {response.json()}"  # noqa

# Testing Add tenant by dwelling_id response code is 422
@pytest.mark.asyncio
async def test_add_tenant_by_dwelling_422(test_app_with_db):
    dwelling_id = "7c1f5da0-bbbe-4625-983d-a08176a09993"

    request_body = {
            "name": "pushpa",
            "mobile": "+917676756311",
            "email": "pushpa@gmail"
        }
    
    headers = {"Authorization": f"Bearer {id_token}"}
    
    response = await test_app_with_db.post(
        f"/api/flats/{dwelling_id}/",
        json=request_body,
        headers=headers,
    )
    assert response.status_code == 422, f"Unexpected response: {response.json()}"  # noqa


# Testing Update tenant by dwelling_id response code is 200
@pytest.mark.asyncio
async def test_update_tenant_by_dwelling(test_app_with_db):
    dwelling_id = "7c1f5da0-bbbe-4625-983d-a08176a09993"

    request_body = {
            "name": "pushpa",
            "mobile": "+917676756312",
            "email": "user@example.com"
        }
    
    headers = {"Authorization": f"Bearer {id_token}"}
    
    response = await test_app_with_db.put(
        f"/api/flats/{dwelling_id}/tenant",
        json=request_body,
        headers=headers,
    )
    assert response.status_code == 200, f"Unexpected response: {response.json()}"  # noqa


# Testing Update tenant by dwelling_id response code is 404
@pytest.mark.asyncio
async def test_update_tenant_by_dwelling_404(test_app_with_db):
    dwelling_id = "7c1f5da0-bbbe-4625-983d-a08176a09994"

    request_body = {
            "name": "pushpa",
            "mobile": "+917676756311",
            "email": "user@example.com"
        }
    
    headers = {"Authorization": f"Bearer {id_token}"}
    
    response = await test_app_with_db.put(
        f"/api/flats/{dwelling_id}/tenant",
        json=request_body,
        headers=headers,
    )
    assert response.status_code == 404, f"Unexpected response: {response.json()}"  # noqa

# Testing Update tenant by dwelling_id response code is 422
@pytest.mark.asyncio
async def test_update_tenant_by_dwelling_422(test_app_with_db):
    dwelling_id = "7c1f5da0-bbbe-4625-983d-a08176a09993"

    request_body = {
            "name": "pushpa",
            "mobile": "+917676756311",
            "email": "pushpa@gmail"
        }
    
    headers = {"Authorization": f"Bearer {id_token}"}
    
    response = await test_app_with_db.put(
        f"/api/flats/{dwelling_id}/tenant",
        json=request_body,
        headers=headers,
    )
    assert response.status_code == 422, f"Unexpected response: {response.json()}"  # noqa


# Testing remove tenant using dwelling id response code 204_NO_CONTENT
@pytest.mark.asyncio
async def test_remove_tenant_204(test_app_with_db):
    dwelling_id = "7c1f5da0-bbbe-4625-983d-a08176a09993"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.delete(
        f"/api/flats/{dwelling_id}/tenant",
        headers=headers,
    )
    assert (
        response.status_code == status.HTTP_204_NO_CONTENT
    ), f"Unexpected response: {response.json()}"


# Testing remove tenant using dwelling id response code 404
@pytest.mark.asyncio
async def test_remove_tenant_404(test_app_with_db):
    dwelling_id = "7c1f5da0-bbbe-4625-983d-a08176a09994"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = await test_app_with_db.delete(
        f"/api/flats/{dwelling_id}/tenant",
        headers=headers,
    )
    assert (
        response.status_code == 404
    ), f"Unexpected response: {response.json()}"