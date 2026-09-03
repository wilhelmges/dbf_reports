from sqlmodel import SQLModel
from dbf_reports.database.db import engine
from dbf_reports.database.dfmodels import  Df1, Df4, Df5
from dbf_reports.database.filehash import FileHash
from hello_world import HelloWorld

def remove_tables(engine):
    SQLModel.metadata.drop_all(engine)

if __name__=="__main__":
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)