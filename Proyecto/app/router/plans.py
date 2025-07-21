from fastapi import APIRouter
from models import Plan
from bd import SessionDep
from sqlmodel import select

router = APIRouter()

@router.post("/plans", tags=['plans'])
async def create_plan(plan_data: Plan, session: SessionDep):
    plan_bd = Plan.model_validate(plan_data.model_dump())
    session.add(plan_bd)
    session.commit()
    session.refresh(plan_bd)
    return plan_bd


@router.get("/plans", tags=['plans'])
async def list_plans(session: SessionDep):
    query = select(Plan)
    plans = session.exec(query).all()
    return plans