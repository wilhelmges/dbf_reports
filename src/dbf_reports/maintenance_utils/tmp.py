from dbf_reports.database.dfmodels import Df1
from dbf_reports.database.hello_world import HelloWorld
from dbf_reports.database.dfmodel_repository import Repository
from dbf_reports.database.db import SessionFactory


with SessionFactory() as session:
    with session.begin():
        h = HelloWorld(title="Hello World")
        session.add(h)
        session.commit()