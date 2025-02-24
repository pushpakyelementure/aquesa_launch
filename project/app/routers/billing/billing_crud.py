from fastapi import HTTPException, status

from app.db.models.community import community_model
from app.db.models.billing import billing_model


async def comm_bill_setup(community_id, **data):
    community = await community_model.find_one(
        community_model.community_id == community_id
    )

    if community is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community Not found",
        )
    
    total_fixed_cost = 0
    for entry in data["fixed_cost"]:
        for key, value in entry.items():
            total_fixed_cost += value

    total_variable_cost = 0
    for entry in data["variable_cost"]:
        for key, value in entry.items():
            total_variable_cost += value

    data["total_fixed_cost"] = total_fixed_cost
    data["total_variable_cost"] = total_variable_cost
    data["community_id"] = community_id  # Ensure it's included
    result = billing_model(**data)
    await result.insert()
    return result


async def read_comm_setup(community_id):
    comm_bill_setup = await billing_model.find_one(billing_model.community_id == community_id) # noqa
    if comm_bill_setup is None:
        raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail="Community not found",
           )
    read_all_comm_setup = await billing_model.find(billing_model.community_id == community_id).to_list() # noqa
    return read_all_comm_setup
    print(read_all_comm_setup)


async def update_comm_bill_setup(community_id, **data):
    comm = await billing_model.find_one(billing_model.community_id == community_id) # noqa
    if comm is None:
        raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail="User not found",
           )
    comm.year = data["year"]
    comm.month = data["month"]

    comm.fixed_cost = data["fixed_cost"]
    total_fixed_cost = 0
    for entry in data["fixed_cost"]:
        for key, value in entry.items():
            total_fixed_cost += value
    comm.total_fixed_cost = total_fixed_cost

    comm.variable_cost = data["variable_cost"]
    total_variable_cost = 0
    for entry in data["variable_cost"]:
        for key, value in entry.items():
            total_variable_cost += value
    comm.total_variable_cost = total_variable_cost
    comm.bill_date = data["bill_date"]
    await comm.save()
    return comm
