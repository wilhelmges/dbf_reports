from sqlmodel import Field, SQLModel

from dbf_reports.database.db import SessionFactory
from dbf_reports.database.base_model import BaseModel
from dbf_reports.database.dfmodel_repository import Repository

class HelloWorld(BaseModel, table=True):
    __tablename__ = "hello_world"
    id: int | None = Field(default=None, primary_key=True)
    title :str | None = Field(default=None)

    @classmethod
    def key_fields(cls):
        return ("title",)

if __name__ == "__main__":
    with SessionFactory() as session:
        r = Repository(session, HelloWorld)
        h = HelloWorld(title="Hello World")
        print(r.find_statement_by_key(h))
        print(r.find_by_key(h))