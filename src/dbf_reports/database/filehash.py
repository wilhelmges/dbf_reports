from decimal import Decimal
from datetime import date
from sqlmodel import SQLModel, Field

class FileHash(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    hash: str
    filepath: str