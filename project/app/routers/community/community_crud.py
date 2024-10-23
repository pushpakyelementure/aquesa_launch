from datetime import datetime

from fastapi import HTTPException, status

from app.db.models.community import community_model


# Create a community document
async def create_community(**data_to_db):

    community_name = await community_model.find_one(
        community_model.community_name == data_to_db["community_name"],
    )
    if community_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="community already exists",
        )

    data = community_model(**data_to_db)
    await data.insert()
    return data


# Read a community document
async def get_community_by_id(community_id):

    comm = await community_model.find_one(community_model.community_id == community_id) # noqa
    print(comm)
    if comm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="community not found",
        )
    return comm


# Read all community documents
async def get_all_community():
    data = await community_model.find_all().to_list()

    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="community not found",
        )
    return data


# Update a community document
async def update_community(community_id, **data):
    comm = await community_model.find_one(community_model.community_id == community_id)  # noqa
    if comm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="community not found",
        )

    comm.community_name = data["community_name"]
    comm.location = data["location"]
    comm.dwelling_types = data["dwelling_types"]
    comm.bill_model = data["bill_model"]
    comm.billing_cycle_date = data["billing_cycle_date"]
    comm.billing_start_date = data["billing_start_date"]
    comm.next_invoice_date = data["next_invoice_date"]
    comm.gst_no = data["gst_no"]
    comm.subscription_status = data["subscription_status"]
    comm.meta.activity = data["meta"]["activity"]

    await comm.save()

    return comm


# patch for change the subscription status [active or inactive]
async def subscription_status(community_id, user_token, **data):
    comm = await community_model.find_one(community_model.community_id == community_id)  # noqa
    print(comm)
    if comm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="community not found",
        )
    comm.meta.activity = {
         "updated_by": user_token["uid"],
         "updated_at": datetime.utcnow(),
            }
    await comm.update({"$set": {"meta.activity": comm.meta.activity}})

    await comm.update({"$set": {**data}})

    return comm


# Delete a community document
async def delete_community(community_id):
    comm = await community_model.find_one(community_model.community_id == community_id)  # noqa

    if comm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="community not found",
        )

    await comm.delete()

    return comm
