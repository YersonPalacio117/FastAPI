from models import Customer, CustomerCreate, CustomerUpdate, Plan, CustomerPlan, Status
from bd import SessionDep
from fastapi import APIRouter, status, HTTPException, Query
from sqlmodel import select


router = APIRouter()


@router.post("/customers", response_model=Customer, tags=['customers'])
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@router.get("/customers/{customer_id}", response_model=Customer, tags=['customers'])
async def read_customer(customer_id: int, session: SessionDep):
    customer_bd = session.get(Customer, customer_id)
    if not customer_bd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El cliente no existe")
    return customer_bd


@router.patch("/customers/{customer_id}", response_model=Customer, status_code=status.HTTP_201_CREATED, tags=['customers'])
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


@router.delete("/customers/{customer_id}", tags=['customers'])
async def delete_customer(customer_id:int, session:SessionDep):
    customer_bd = session.get(Customer, customer_id)
    if not customer_bd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El cliente no existe")
    session.delete(customer_bd)
    session.commit()
    return {"detail" : "Ok"}


@router.get("/customers", response_model=list[Customer], tags=['customers'])
async def list_customer(session: SessionDep):
    return session.exec(select(Customer)).all()


@router.post("/customers/{customer_id}/plans/{plan_id}", tags=['customers'])
async def suscribe_customer_plan(
    customer_id: int, plan_id: int, session: SessionDep, 
    plan_status: Status = Query()
    ):
    customer_bd = session.get(Customer, customer_id)
    if not customer_bd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El cliente no existe")
    plan_bd = session.get(Plan, plan_id)
    if not plan_bd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El plan no existe")
    customer_plan_bd = CustomerPlan(customer_id=customer_bd.id, plan_id=plan_bd.id, status=plan_status)
    session.add(customer_plan_bd)
    session.commit()
    session.refresh(customer_plan_bd)
    return customer_plan_bd


@router.get("/customers/{customer_id}/plans", tags=['customers'])
async def list_customer_plans(customer_id: int, session: SessionDep, plan_status: Status = Query()):
    customer_bd = session.get(Customer, customer_id)
    if not customer_bd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El cliente no existe")
    
    query = (
        select(CustomerPlan)
        .where(CustomerPlan.customer_id == customer_id)
        .where(CustomerPlan.status == plan_status)
    )
    customer_plans = session.exec(query).all()
    return customer_plans

