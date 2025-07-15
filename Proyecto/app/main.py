import zoneinfo
from fastapi import FastAPI
from datetime import datetime
from bd import create_all_tables
from .router import customers, transactions, invoices

app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(invoices.router)


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


