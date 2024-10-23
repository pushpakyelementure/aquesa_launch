from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import UUID4
from typing import List
import uuid

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import io
import os
import boto3

from app.auth import verify
from app.auth.permissions import authorize
from app.routers.subscription import (
    subscription_res_schema,
    subscription_req_schema,
)  # noqa
from app.db.models.community import community_model
from app.routers.subscription import subscription_crud
from app.routers.subscription.subscription_res_docs import (
    create_invoice,
    read_invoice,
    readall_invoice,
    update_invoice,
    gen_invoice,
)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("REGION_NAME"),
)

router = APIRouter()


def upload_to_s3(buffer, bucket_name, key):
    s3_client.upload_fileobj(buffer, bucket_name, key)


def generate_invoice():
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Add data to the PDF
    c.drawString(100, 750, "Invoice")
    c.drawString(100, 730, "Date: october 12, 2024")
    c.drawString(100, 710, "Invoice Number: 123456")
    data = [
        ["Community", "bill_amount"],
        ["Engrace", "20000"],
        ["Soulace", "15000"],
        ["Soultree", "24000"]
    ]

    # Draw a table
    for row_idx, row in enumerate(data):
        for col_idx, cell in enumerate(row):
            c.drawString(100 + col_idx * 100, 650 - row_idx * 20, cell)
    c.save()
    buffer.seek(0)
    return buffer


# Create a Subscription invoice for particular community
@router.post(
    "/{community_id}",
    response_model=subscription_res_schema.subscription_res,
    status_code=status.HTTP_201_CREATED,
    responses=create_invoice.responses,
)
async def create_invoice(
    community_id: UUID4,
    req: subscription_req_schema.create_subscription,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser_or_admin(
        user_token,
    )
    community = await community_model.find_one(
        community_model.community_id == community_id
    )
    if community is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community Not found",
        )
    data = {
        "community_id": community_id,
        "subscription_invoice_id": str(uuid.uuid4()),
        "month": req.month,
        "subscription_plan": req.subscription_plan,
        "billing_amount": req.billing_amount,
        "invoice_date": req.invoice_date,
        "payment_due_date": req.payment_due_date,
    }

    try:
        await subscription_crud.create_invoice(**data)
        return {
            "detail": "Invoice created successfully",
        }
    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Generate invoice
@router.post(
    "/{community_id}/{subscription_invoice_id}",
    response_model=subscription_res_schema.subscription_res,
    status_code=status.HTTP_201_CREATED,
    responses=gen_invoice.responses,
)
async def generates_invoice(
    community_id: UUID4,
    subscription_invoice_id: UUID4,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser_or_admin(
        user_token,
    )
    bucket_name = os.getenv("BUCKET_NAME")
    key = user_token["uid"]
    upload_to_s3(generate_invoice(), bucket_name, key)
    url = s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": bucket_name,
            "Key": user_token["uid"],
        },
        ExpiresIn=3600,
    )
    print(url)

    try:
        await subscription_crud.generate_invoice(community_id, subscription_invoice_id, url)  # noqa
        return {
            "detail": "Invoice generate successfully",
        }
    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Read All the subscription invoices for specified community
@router.get(
    "/{community_id}",
    response_model=List[subscription_res_schema.get_all_invoices],
    status_code=status.HTTP_200_OK,
    responses=readall_invoice.responses,
)
async def get_all_invoices(
    community_id: UUID4,
    user_token=Depends(verify.get_user_token)
):
    await authorize.user_is_superuser_or_admin(
        user_token,
    )
    # Retrieve all the invoices for the community
    try:
        sub_invoice = await subscription_crud.read_invoice(community_id)
        return sub_invoice
    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Update a invoice data for the particular invoice id
@router.put(
    "/{community_id}/{subscription_invoice_id}",
    response_model=subscription_res_schema.subscription_res,
    status_code=status.HTTP_200_OK,
    responses=update_invoice.responses,
)
async def update_invoice(
    community_id: UUID4,
    subscription_invoice_id: UUID4,
    req: subscription_req_schema.update_subscription,
    user_token=Depends(verify.get_user_token),
):
    await authorize.user_is_superuser_or_admin(
        user_token,
    )
    data = {
        "month": req.month,
        "subscription_plan": req.subscription_plan,
        "billing_amount": req.billing_amount,
        "invoice_date": req.invoice_date,
        "payment_due_date": req.payment_due_date,
    }

    try:
        await subscription_crud.update_invoice(
            community_id, subscription_invoice_id, **data
        )  # noqa
        return {
            "detail": "Invoice updated successfully",
        }
    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Download the invoice
@router.get(
    "/{community_id}/{subscription_invoice_id}/download",
    response_model=subscription_res_schema.download_invoices,
    status_code=status.HTTP_200_OK,
    responses=read_invoice.responses,
)
async def download_invoice(
    community_id: UUID4,
    subscription_invoice_id: UUID4,
    user_token=Depends(verify.get_user_token)
):
    await authorize.user_is_superuser_or_admin(
        user_token,
    )
    try:
        gen_invoice = await subscription_crud.download_invoice(community_id, subscription_invoice_id)  # noqa
        print(gen_invoice.invoice_url)
        return gen_invoice
    except Exception as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
