from fastapi import HTTPException, status

from app.db.models.support import service_request


# Create a service request ticket
async def post_ticket(**data_to_db):
    data = service_request(**data_to_db)
    await data.insert()


# Read ticket by dwelling_id
async def get_by_dwelling_id(dwelling_id):
    dwell = await service_request.find_one(service_request.dwelling_id == dwelling_id)# noqa
    if dwell is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="dwelling not found",
        )
    support = await service_request.find(service_request.dwelling_id == dwelling_id).to_list()  # noqa
    return support


# Read a ticket by sr_id
async def get_by_sr_id(sr_id):
    service_ticket = await service_request.find_one(service_request.sr_id == sr_id) # noqa
    if service_ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    return service_ticket


# Read all ticket
async def get_all_tickets(community_id):
    comm = await service_request.find_one(service_request.community_id == community_id)# noqa
    if comm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community not found",
        )
    tickets = await service_request.find(service_request.community_id == community_id).to_list() # noqa
    
    return tickets
