from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from typing import Optional

class CustomerBase(SQLModel):
    name: str
    description: Optional[str] = None
    email: str
    age: int

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class CustomerUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None

class Transaction(BaseModel):
    id: int
    ammount: int
    description: str

class Invoice(BaseModel):
    id: int
    customer: Customer
    transaction: list[Transaction]
    total: int
    
    @property
    def ammount_total(self):
        return sum(transaction.ammount for transaction in self.transaction)
