# import os
# import pytest
# from fastapi import status
# from app.auth import manage
# from tests.utils import get_token


# id_token = get_token.login_and_get_id_token(
#     os.getenv("FIREBASE_SUPERUSER_ADMIN_EMAIL"),
#     os.getenv("FIREBASE_SUPERUSER_ADMIN_PASSWORD"),
# )


# # Testing for total consumption of one community response code is 200
# @pytest.mark.asyncio
# async def test_get_total_csm(test_app_with_db):
#     headers = {"Authorization": f"Bearer {id_token}"}
#     community_id = "9d12da45-8a93-45b1-976c-1bfc4ea27c08"

#     params = {
#         "start_date": "2025-02-21 00:00:00",
#         "end_date": "2025-02-21 23:59:59",
#         "aggregation": "day",
#     }

#     response = await test_app_with_db.get(
#         f"/api/consumption/consumption/{community_id}",  # noqa
#         headers=headers,
#         params=params,  # Using query parameters
#     )

#     assert response.status_code == 200, f"Unexpected response: {response.json()}"  # noqa

#     assert response.json()["total_consumption"] == 2438


# # Testing for total consumption of one community response code is 404
# @pytest.mark.asyncio
# async def test_get_total_csm_404(test_app_with_db):
#     headers = {"Authorization": f"Bearer {id_token}"}
#     community_id = "9d12da45-8a93-45b1-976c-1bfc4ea27c09"

#     params = {
#         "start_date": "2025-02-21 00:00:00",
#         "end_date": "2025-02-21 23:59:59",
#         "aggregation": "day",
#     }

#     response = await test_app_with_db.get(
#         f"/api/consumption/consumption/{community_id}",  
#         headers=headers,
#         params=params,  # Using query parameters
#     )

#     assert response.status_code == 404, f"Unexpected response: {response.json()}"  # noqa

# # Testing for total consumption of one community response code is 422
# @pytest.mark.asyncio
# async def test_get_total_csm_422(test_app_with_db):
#     headers = {"Authorization": f"Bearer {id_token}"}
#     community_id = "9d12da45-8a93-45b1-976c-1bfc4ea27c08"

#     params = {
#         "start_date": "2025-02-21 00:00:00",
#         "end_date": "20-02-2025 23:59:59", # date format is not supported
#         "aggregation": "day",
#     }

#     response = await test_app_with_db.get(
#         f"/api/consumption/consumption/{community_id}",  # noqa
#         headers=headers,
#         params=params,  # Using query parameters
#     )

#     assert response.status_code == 422, f"Unexpected response: {response.json()}"  # noqa


# # Testing for top 5 dwelling consumption in community  response code is 200
# @pytest.mark.asyncio
# async def test_get_top_dwellings(test_app_with_db):
#     headers = {"Authorization": f"Bearer {id_token}"}
#     community_id = "9d12da45-8a93-45b1-976c-1bfc4ea27c08"

#     params = {
#         "start_date": "2025-02-23 00:00:00",
#         "end_date": "2025-02-23 23:59:59",
#         "aggregation": ["day", "week", "month"],
#     }

#     response = await test_app_with_db.get(
#         f"/api/consumption/top-dwellings/{community_id}",  # noqa
#         headers=headers,
#         params=params,  # Using query parameters
#     )
#     assert response.status_code == 200, f"Unexpected response: {response.json()}" # noqa


# # Testing for top 5 dwelling consumption in community  response code is 422
# @pytest.mark.asyncio
# async def test_get_top_dwellings_422(test_app_with_db):
#     headers = {"Authorization": f"Bearer {id_token}"}
#     community_id = "9d12da45-8a93-45b1-976c-1bfc4ea27c08"
#     params = {
#         "start_date": "2025-02-23 00:00:00",
#         "end_date": "23-02-2025 23:59:59",
#         "aggregation": "day",
#     }

#     response = await test_app_with_db.get(
#         f"/api/consumption/top-dwellings/{community_id}",  # noqa
#         headers=headers,
#         params=params,  # Using query parameters
#     )
#     assert response.status_code == 422, f"Unexpected response: {response.json()}" # noqa


# # Testing for top 5 dwelling consumption in community  response code is 404
# @pytest.mark.asyncio
# async def test_get_top_dwellings_404(test_app_with_db):
#     headers = {"Authorization": f"Bearer {id_token}"}
#     community_id = "9d12da45-8a93-45b1-976c-1bfc4ea27c09"

#     params = {
#         "start_date": "2025-02-23 00:00:00",
#         "end_date": "2025-02-23 23:59:59",
#         "aggregation": ["day", "week", "month"],
#     }

#     response = await test_app_with_db.get(
#         f"/api/consumption/top-dwellings/{community_id}",
#         headers=headers,
#         params=params,
#     )
#     assert response.status_code == 404 , f"Unexpected response: {response.json()}" # noqa
