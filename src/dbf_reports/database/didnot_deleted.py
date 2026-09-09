from decimal import Decimal
from datetime import date
from sqlmodel import SQLModel, Field

from dbf_reports.database.base_model import BaseModel

class Df1(BaseModel, table=True):
    __tablename__ = "didnot_deleted"

    id: int | None = Field(default=None, primary_key=True)
    row: int
    file: str
