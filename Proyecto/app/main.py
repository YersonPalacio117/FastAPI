import zoneinfo
from fastapi import FastAPI, Request
from datetime import datetime
from bd import create_all_tables
from .router import customers, transactions, invoices, plans
import time

app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(invoices.router)
app.include_router(plans.router)


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    end_time = time.time() 
    print(f"Request {request.url} time: {end_time - start_time} seconds")
    return response

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
async def get_time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time" : datetime.now(tz)}


