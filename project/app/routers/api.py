from fastapi import APIRouter

from app.routers.admin import admin_endpoint
from app.routers.app_users import app_endpoint
from app.routers.auth import auth_endpoint
from app.routers.community import community_endpoint
from app.routers.community_users import community_users_endpoint
# from app.routers.consumption import consumption_endpoint
from app.routers.devices import device_endpoint
from app.routers.dwelling import dwelling_endpoint
from app.routers.subscription import subscription_endpoint
# from app.routers.valve_management import valve_management_endpoint

router = APIRouter()

router.include_router(
    admin_endpoint.router,
    prefix="/admin",
    tags=["Admin APIs"],
)

router.include_router(
    community_users_endpoint.router,
    prefix="/community_users",
    tags=["Community Users APIs"],
)

router.include_router(
    app_endpoint.router,
    prefix="/app_users",
    tags=["App Users APIs"],
)

router.include_router(
    community_endpoint.router,
    prefix="/community",
    tags=["Community APIs"],
)

router.include_router(
    dwelling_endpoint.router,
    prefix="/dwelling",
    tags=["Dwelling APIs"],
)

router.include_router(
    device_endpoint.router,
    prefix="/device",
    tags=["Devices APIs"],
)


# router.include_router(
#     consumption_endpoint.router,
#     prefix="/consumption",
#     tags=["Consumption APIs"],
# )

router.include_router(
    subscription_endpoint.router,
    prefix="/subscription",
    tags=["Subscription APIs"],
)

# router.include_router(
#     valve_management_endpoint.router,
#     prefix="/valve",
#     tags=["Valve Management APIs"],
# )

router.include_router(
    auth_endpoint.router,
    prefix="/auth",
    tags=["Auth APIs"],
)