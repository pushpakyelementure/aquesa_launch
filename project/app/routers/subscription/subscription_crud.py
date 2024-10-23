from fastapi import HTTPException, status

from app.db.models.subscription import subscription


# Create a new community user information
async def create_invoice(**data):
    result = subscription(**data)
    await result.insert()


# Read all subscription information
async def read_invoice(community_id):
    invoice = await subscription.find_one(
        subscription.community_id == community_id
    )

    if invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community Not found",
        )
    read_data = await subscription.find_all().to_list()
    if read_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Users not found",
        )
    return read_data


# Update subscription information
async def update_invoice(community_id, subscription_invoice_id, **data):
    comm = await subscription.find_one(
        subscription.community_id == community_id
    )
    if comm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community Not found",
        )
    invoice = await subscription.find_one(
        subscription.subscription_invoice_id == subscription_invoice_id
    )
    if invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="invoice Not found",
        )
    invoice.month = data["month"]
    invoice.subscription_plan = data["subscription_plan"]
    invoice.billing_amount = data["billing_amount"]
    invoice.invoice_date = data["invoice_date"]
    invoice.payment_due_date = data["payment_due_date"]

    await invoice.save()
    return invoice


# Generate the invoice
async def generate_invoice(community_id, subscription_invoice_id, url):
    comm = await subscription.find_one(
        subscription.community_id == community_id
    )
    if comm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community Not found",
        )
    invoice = await subscription.find_one(
        subscription.subscription_invoice_id == subscription_invoice_id
    )
    if invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="invoice Not found",
        )
    await invoice.update({"$set": {"invoice_url": url}})
    return invoice


# Download invoice
async def download_invoice(community_id, subscription_invoice_id):
    comm = await subscription.find_one(
        subscription.community_id == community_id
    )
    if comm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community Not found",
        )
    invoice = await subscription.find_one(
        subscription.subscription_invoice_id == subscription_invoice_id
    )
    if invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="invoice Not found",
        )
    return invoice
