from models import Invoice
from fastapi import APIRouter


router = APIRouter()


@router.post("/invoices", tags=['invoices'])
async def create_invoices(invoice_data: Invoice):
    return invoice_data