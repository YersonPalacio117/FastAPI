from fastapi import APIRouter
from models import Transaction


router = APIRouter()


@router.post("/transaction", tags=['transactions'])
async def create_transaction(transaction_data: Transaction):
    return transaction_data