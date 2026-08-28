from sqlmodel import SQLModel
from src.dbf_reports.database.db import engine
from src.dbf_reports.database.models import FileHash, Df1, Df4, Df5


def remove_tables(engine):
    SQLModel.metadata.drop_all(engine)

if __name__=="__main__":
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)