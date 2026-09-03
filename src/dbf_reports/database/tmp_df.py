from sqlmodel import Field, SQLModel, select

from dbf_reports.database.db import SessionFactory
from dbf_reports.database.dfmodels import Df1
from dbf_reports.database.dfmodel_repository import Repository


if __name__ == "__main__":
    with SessionFactory() as session:
        r = Repository(session, Df1)
        statement = select(Df1).limit(1)
        d = session.exec(statement).first()
        print(d)

        print(r.find_statement_by_key(d))
        print(r.find_by_key(d))