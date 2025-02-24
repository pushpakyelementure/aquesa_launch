import beanie
import motor
import motor.motor_asyncio

from app.db.models import admin_user, app_user, community, valve_status
from app.db.models import community_user, dwelling, subscription, csm_limit
from app.db.models import billing, notification, support, alert, consumption


async def init_db(db_uri: str, db_name: str):
    client = motor.motor_asyncio.AsyncIOMotorClient(
        db_uri,
        uuidRepresentation="standard",
    )

    await beanie.init_beanie(
        database=client[db_name],
        document_models=[
            community.community_model,
            admin_user.admin_user_model,
            community_user.community_users_model,
            app_user.app_users_model,
            dwelling.dwelling_model,
            subscription.subscription,
            csm_limit.day_limit,
            valve_status.device_status,
            billing.billing_model,
            notification.notifications,
            support.service_request,
            alert.alert_model,
            consumption.rawdata
        ],
    )
