from fastapi import HTTPException, status
from datetime import datetime

from app.db.models.alert import alert_model



async def create_alert_data(**data):

    latest_data = await data_collection.find().sort("datatime", -1).limit(1).to_list(1)
    # Extracting necessary fields
    device_id = payload.get("data", {}).get("devId", "Unknown")
    event_time = payload.get("data", {}).get("evt", {}).get("etm", "Unknown")
    csm_value = payload.get("data", {}).get("evt", {}).get("csm", 0)  # Default to 0 if missing
    severity = get_severity(csm_value)
    alert = {
        "device_id": device_id,
        "timestamp": event_time,
        "message": f"Water leakage detected with severity {severity} (csm: {csm_value})"
    }
    result = await collection.insert_one(alert)

    data = alert_model(**result)
    await data.insert()
    return data
