from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from datetime import datetime
from typing import List

from app.auth import verify

from app.auth.permissions import authorize
from app.routers.support import support_crud
from app.routers.support import support_req_schema, support_res_schema
from app.db.models.dwelling import dwelling_model
from app.routers.support.support_res_docs import (
    get_dwelling,
    get_sr_id,
    get_tickets,
    create_ticket,
)


router = APIRouter()


# Read all tickets
@router.get(
    "/support/{community_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[support_res_schema.get_tickets],
    responses=get_tickets.responses,
)
async def get_all_tickets(
    community_id: UUID4,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser(
        user_token=user_token,
    )
    try:
        comm = await support_crud.get_all_tickets(community_id)
        return [{
            "sr_id": support.sr_id,
            "community_id": support.community_id,
            "dwelling_id": support.dwelling_id,
            "date": support.date,
            "category": support.category,
            "description": support.description,
            "status": support.status,
            "documents": support.documents,
            "timeline": support.timeline,
            "meta": support.meta,
        }for support in comm
        ]
    except Exception as http_ex:
        raise http_ex

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Read a ticket by sr_id
@router.get(
    "/{sr_id}",
    status_code=status.HTTP_200_OK,
    response_model=support_res_schema.get_sr_id,
    responses=get_sr_id.responses,
)
async def get_ticket_info(
    sr_id: str,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser(
        user_token=user_token,
    )
    try:
        ticket_info = await support_crud.get_by_sr_id(sr_id)
        print(ticket_info)
        return {
            "sr_id": ticket_info.sr_id,
            "community_id": ticket_info.community_id,
            "dwelling_id": ticket_info.dwelling_id,
            "date": ticket_info.date,
            "category": ticket_info.category,
            "description": ticket_info.description,
            "status": ticket_info.status,
            "documents": ticket_info.documents,
            "timeline": ticket_info.timeline,
            "meta": ticket_info.meta,
        }
    except Exception as http_ex:
        raise http_ex
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Create a tickets for dwelling
@router.post(
    "/{community_id}/{dwelling_id}",
    status_code=status.HTTP_200_OK,
    response_model=support_res_schema.create_ticket,
    responses=create_ticket.responses,
)
async def create_ticket(
    community_id: UUID4,
    dwelling_id: UUID4,
    req: support_req_schema.service_request,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser(
            user_token=user_token,
    )
    community = await dwelling_model.find_one(
        dwelling_model.community_id == community_id
    )
    if community is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community Not found",
        )
    dwell = await dwelling_model.find_one(dwelling_model.dwelling_id == dwelling_id)  # noqa
    if dwell is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dwelling Not found",
        )
    # Create timeline list
    timeline_info = []
    for timeline_data in req.timeline:
        time_info = {
            "name": timeline_data.name,
            "date": datetime.utcnow(),
            "description": timeline_data.description,
            "document": timeline_data.document,
        }
        timeline_info.append(time_info)
    data = {
        "sr_id": req.sr_id,
        "community_id": community_id,
        "dwelling_id": dwelling_id,
        "date": datetime.utcnow(),
        "category": req.category,
        "description": req.description,
        "status": req.status,
        "documents": req.documents,
        "timeline": timeline_info,
        "meta": {
            "created_at": datetime.utcnow(),
            "created_by": user_token["uid"],
        },
    }
    try:
        await support_crud.post_ticket(**data)
        return {
            "detail": "Ticket created successfully",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Read all tickets by Dwelling_id
@router.get(
    "/dwelling/{dwelling_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[support_res_schema.get_tickets],
    responses=get_dwelling.responses,
)
async def get_tickets_by_dwelling(
    dwelling_id: UUID4,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser(
        user_token=user_token,
    )
    try:
        tickets = await support_crud.get_by_dwelling_id(dwelling_id)  # noqa
        return tickets

    except Exception as http_ex:
        raise http_ex
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
