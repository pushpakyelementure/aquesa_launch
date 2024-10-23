# import os
# import pytest
# from fastapi import status

# from tests.utils import get_token

# id_token = get_token.login_and_get_id_token(
#     os.getenv("FIREBASE_SUPERUSER_ADMIN_EMAIL"),
#     os.getenv("FIREBASE_SUPERUSER_ADMIN_PASSWORD"),
# )


# # Testing Create a new subscription response code 201_CREATED
# @pytest.mark.asyncio
# async def test_create_201_subscription(test_app_with_db):
#     request_body = {
#         "month": "2024-04-16",
#         "subscription_plan": "active",
#         "billing_amount": 5000,
#         "invoice_date": "2024-04-16",
#         "payment_due_date": "2024-04-16",
#     }
#     global community_id
#     community_id = "27d61e61-f5d3-4252-9383-f2559cb4444b"
#     headers = {"Authorization": f"Bearer {id_token}"}
#     response = await test_app_with_db.post(
#         f"/api/subscription/{community_id}",
#         json=request_body,
#         headers=headers,
#     )
#     assert (
#         response.status_code == status.HTTP_201_CREATED
#     ), f"Unexpected response: {response.json()}"


# # Testing Create a new subscription response code 404_NOT_FOUND
# @pytest.mark.asyncio
# async def test_create_404_subscription(test_app_with_db):
#     request_body = {
#         "month": "2024-04-16",
#         "subscription_plan": "active",
#         "billing_amount": 5000,
#         "invoice_date": "2024-04-16",
#         "payment_due_date": "2024-04-16",
#     }
#     community = "6201419a-9834-46aa-bde8-62452d6928d0"
#     headers = {"Authorization": f"Bearer {id_token}"}
#     response = await test_app_with_db.post(
#         f"/api/subscription/{community}",
#         json=request_body,
#         headers=headers,
#     )
#     assert (
#         response.status_code == status.HTTP_404_NOT_FOUND
#     ), f"Unexpected response: {response.json()}"


# # Testing Create a new subscription response code 422_UNPROCESSABLE_ENTITY
# @pytest.mark.asyncio
# async def test_create_422_subscription(test_app_with_db):
#     request_body = {
#         "month": "2024-04-16",
#         "subscription_plan": "act",
#         "billing_amount": 5000,
#         "invoice_date": "2024-04-16",
#         "payment_due_date": "2024-04-16",
#     }
#     headers = {"Authorization": f"Bearer {id_token}"}
#     response = await test_app_with_db.post(
#         f"/api/subscription/{community_id}",
#         json=request_body,
#         headers=headers,
#     )
#     assert (
#         response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
#     ), f"Unexpected response: {response.json()}"


# # Testing Read a subscription response code 404_NOT_FOUND
# @pytest.mark.asyncio
# async def test_read_404_subscription(test_app_with_db):
#     community = "6201419a-9834-46aa-bde8-62452d6928d0"
#     headers = {"Authorization": f"Bearer {id_token}"}
#     response = await test_app_with_db.get(
#         f"/api/subscription/{community}",
#         headers=headers,
#     )
#     assert (
#         response.status_code == status.HTTP_404_NOT_FOUND
#     ), f"Unexpected response: {response.json()}"


# # Testing Create generate invoice response code 201_CREATED
# @pytest.mark.asyncio
# async def test_generate_invoice_201_subscription(test_app_with_db):
#     subscription_invoice_id = "5b7f19ba-9b91-4364-aae2-44feb68f880c"
#     headers = {"Authorization": f"Bearer {id_token}"}
#     response = await test_app_with_db.post(
#         f"/api/subscription/{community_id}/{subscription_invoice_id}",  # noqa
#         headers=headers,
#         params={"subscription_invoice_id": subscription_invoice_id},
#     )
#     assert (
#         response.status_code == status.HTTP_201_CREATED
#     ), f"Unexpected response: {response.json()}"


# # Testing Create invalid community for generate invoice 404_NOT_FOUND
# @pytest.mark.asyncio
# async def test_generate_invoice_404_subscription(test_app_with_db):
#     community = "6201419a-9834-46aa-bde8-62452d6928d0"
#     subscription_invoice_id = "5b7f19ba-9b91-4364-aae2-44feb68f880c"
#     headers = {"Authorization": f"Bearer {id_token}"}
#     response = await test_app_with_db.post(
#         f"/api/subscription/{community}/{subscription_invoice_id}",  # noqa
#         headers=headers,
#         params={"subscription_invoice_id": subscription_invoice_id},
#     )
#     assert (
#         response.status_code == status.HTTP_404_NOT_FOUND
#     ), f"Unexpected response: {response.json()}"


# # Testing update subscription details response code 200
# @pytest.mark.asyncio
# async def test_update_200_subscription(test_app_with_db):
#     request_body = {
#         "month": "2024-04-16",
#         "subscription_plan": "active",
#         "billing_amount": 500,
#         "invoice_date": "2024-04-16",
#         "payment_due_date": "2024-04-16",
#     }
#     subscription_invoice_id = "5b7f19ba-9b91-4364-aae2-44feb68f880c"
#     headers = {"Authorization": f"Bearer {id_token}"}
#     response = await test_app_with_db.put(
#         f"/api/subscription/{community_id}/{subscription_invoice_id}", # noqa
#         json=request_body,
#         params={"subscription_invoice_id": subscription_invoice_id},
#         headers=headers,
#     )
#     assert (
#         response.status_code == status.HTTP_200_OK
#     ), f"Unexpected response: {response.json()}"


# # Testing update subscription details response code 404
# @pytest.mark.asyncio
# async def test_update_404_subscription(test_app_with_db):
#     request_body = {
#         "month": "2024-04-16",
#         "subscription_plan": "active",
#         "billing_amount": 500,
#         "invoice_date": "2024-04-16",
#         "payment_due_date": "2024-04-16",
#     }
#     community = "6201419a-9834-46aa-bde8-62452d6928d0"
#     subscription_invoice_id = "5b7f19ba-9b91-4364-aae2-44feb68f880c"
#     headers = {"Authorization": f"Bearer {id_token}"}
#     response = await test_app_with_db.put(
#         f"/api/subscription/{community}/{subscription_invoice_id}", # noqa
#         json=request_body,
#         params={"subscription_invoice_id": subscription_invoice_id},
#         headers=headers,
#     )
#     assert (
#         response.status_code == status.HTTP_404_NOT_FOUND
#     ), f"Unexpected response: {response.json()}"


# # Testing update subscription details response code 422_UNPROCESSABLE_ENTITY
# @pytest.mark.asyncio
# async def test_update_422_subscription(test_app_with_db):
#     request_body = {
#         "month": "2024-04-16",
#         "subscription_plan": "act",
#         "billing_amount": 20000,
#         "invoice_date": "2024-04-16",
#         "payment_due_date": "2024-04-16",
#     }
#     subscription_invoice_id = "5b7f19ba-9b91-4364-aae2-44feb68f880c"
#     headers = {"Authorization": f"Bearer {id_token}"}
#     response = await test_app_with_db.put(
#         f"/api/subscription/{community_id}/{subscription_invoice_id}",
#         json=request_body,
#         params={"subscribtion_invoice_id": subscription_invoice_id},
#         headers=headers,
#     )
#     assert (
#         response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
#     ), f"Unexpected response: {response.json()}"


# # Testing Read a subscription response code 200_ok
# @pytest.mark.asyncio
# async def test_read_200_subscription(test_app_with_db):
#     headers = {"Authorization": f"Bearer {id_token}"}
#     response = await test_app_with_db.get(
#         f"/api/subscription/{community_id}",
#         headers=headers,
#     )
#     assert (
#         response.status_code == status.HTTP_200_OK
#     ), f"Unexpected response: {response.json()}"


# # Testing download invoice response code 200
# @pytest.mark.asyncio
# async def test_download_invoice_200_subscription(test_app_with_db):
#     subscription_invoice_id = "5b7f19ba-9b91-4364-aae2-44feb68f880c"
#     headers = {"Authorization": f"Bearer {id_token}"}
#     response = await test_app_with_db.get(
#         f"/api/subscription/{community_id}/{subscription_invoice_id}/download",  # noqa
#         headers=headers,
#     )
#     assert (
#         response.status_code == status.HTTP_200_OK
#     ), f"Unexpected response: {response.json()}"


# # Testing download invoice response code 404_NOT_FOUND
# @pytest.mark.asyncio
# async def test_download_invoice_404_subscription(test_app_with_db):
#     community = "6201419a-9834-46aa-bde8-62452d6928d0"
#     subscription_invoice_id = "5b7f19ba-9b91-4364-aae2-44feb68f880c"
#     headers = {"Authorization": f"Bearer {id_token}"}
#     response = await test_app_with_db.get(
#         f"/api/subscription/{community}/{subscription_invoice_id}/download",
#         headers=headers,
#     )
#     assert (
#         response.status_code == status.HTTP_404_NOT_FOUND
#     ), f"Unexpected response: {response.json()}"
