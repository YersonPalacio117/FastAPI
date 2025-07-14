import zoneinfo
from fastapi import FastAPI
from datetime import datetime
from models import Customer, Transaction, Invoice, CustomerCreate
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


@app.get("/customers", response_model=list[Customer])
async def list_customer(session: SessionDep):
    return session.exec(select(Customer)).all()


@app.post("/transaction")
async def create_transaction(transaction_data: Transaction):
    return transaction_data


@app.post("/invoices")
async def create_invoices(invoice_data: Invoice):
    return invoice_data

