from sqlmodel import SQLModel, Session
from bd import engine
from models import Customer, Transaction

# Asegura que las tablas estén creadas
SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    customer = Customer(
        name="Luis",
        description="Profe Platzi",
        email="hola@lcmartinez.com",
        age=33,
    )
    session.add(customer)
    session.commit()
    session.refresh(customer)

    for x in range(100):
        session.add(
            Transaction(
                customer_id=customer.id,
                description=f"Test number {x}",
                ammount=10 * x,
            )
        )
    session.commit()
