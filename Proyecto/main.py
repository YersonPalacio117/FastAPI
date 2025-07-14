import zoneinfo
from fastapi import FastAPI, HTTPException, status
from datetime import datetime
from models import Customer, Transaction, Invoice, CustomerCreate, CustomerUpdate
from bd import SessionDep, create_all_tables
from sqlmodel import select

app = FastAPI(lifespan=create_all_tables)


@app.get("/")
async def root():
    return {"Mensaje" : "Hola Mundo!"}


country_timezones = {
    'CO' : 'America/Bogota',
    'MX' : 'America/Mexico_City',
    'PE' : 'America/Lima',
    'AR' : 'America/Argentina/Buenos_Aires',
}


@app.get("/time/{iso_code}")
async def time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time" : datetime.now(tz)}


@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@app.get("/customers/{customer_id}", response_model=Customer)
async def read_customer(customer_id: int, session: SessionDep):
    customer_bd = session.get(Customer, customer_id)
    if not customer_bd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El cliente no existe")
    return customer_bd


@app.patch("/customers/{customer_id}", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def modify_customer(customer_id: int, customer_data:CustomerUpdate, session: SessionDep):
    customer_bd = session.get(Customer, customer_id)
    if not customer_bd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El cliente no existe")
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer_bd.sqlmodel_update(customer_data_dict)
    session.add(customer_bd)
    session.commit()
    session.refresh(customer_bd)
    return customer_bd


@app.delete("/customers/{customer_id}")
async def delete_customer(customer_id:int, session:SessionDep):
    customer_bd = session.get(Customer, customer_id)
    if not customer_bd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El cliente no existe")
    session.delete(customer_bd)
    session.commit()
    return {"detail" : "Ok"}


@app.get("/customers", response_model=list[Customer])
async def list_customer(session: SessionDep):
    return session.exec(select(Customer)).all()


@app.post("/transaction")
async def create_transaction(transaction_data: Transaction):
    return transaction_data


@app.post("/invoices")
async def create_invoices(invoice_data: Invoice):
    return invoice_data

