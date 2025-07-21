from fastapi import APIRouter, HTTPException, status
from models import Transaction, TransactionCreate, Customer
from bd import SessionDep
from sqlmodel import select

router = APIRouter()


@router.post("/transaction", tags=['transactions'])
async def create_transaction(transaction_data: TransactionCreate, session: SessionDep):
    transaction_data_dict = transaction_data.model_dump()
    customer = session.get(Customer, transaction_data_dict['customer_id'])

    if not customer:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Customer not found")

    transaction_bd = Transaction.model_validate(transaction_data_dict)
    session.add(transaction_bd)
    session.commit()
    session.refresh(transaction_bd)
    return transaction_bd

@router.get("/transaction/{transaction_id}", tags=['transactions'])
async def list_transaction(session: SessionDep):
    query = select(Transaction)
    transactions = session.exec(query).all()
    return transactions
    