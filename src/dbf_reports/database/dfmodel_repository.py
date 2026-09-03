from typing import TypeVar, Generic
from sqlmodel import SQLModel, Session, select

from dbf_reports.database.dfmodels import Df1
from dbf_reports.database.base_model import BaseModel
T = TypeVar("T", bound=BaseModel)

class Repository(Generic[T]):
    def __init__(self, session: Session, model: type[T]):
        self.session = session
        self.model = model

    def find_statement_by_key(self, obj: T):
        conditions = []
        for field_name in self.model.key_fields():
            value = getattr(obj, field_name)
            conditions.append(
                getattr(self.model, field_name) == value
            )
        return select(self.model).where(*conditions)

    def find_by_key(self, obj: T) -> T | None:
        statement = self.find_statement_by_key(obj)
        return self.session.exec(statement).scalar_one_or_none()

class Df1Repository(Repository[Df1]):
    def __init__(self, session: Session):
        super().__init__(session, Df1)


    def get_select_for_Df1(self):
        return select(Df1).where(
            Df1.NUMIDENT == self.row.NUMIDENT,
            Df1.PERIOD_M == self.row.PERIOD_M,
            Df1.PERIOD_Y == self.row.PERIOD_Y,
            Df1.PAY_YEAR == self.row.PAY_YEAR,
            Df1.PAY_MNTH == self.row.PAY_MNTH,
        )

    def inc_or_createDf1(self):
        if not isinstance(self.row, Df1):
            raise Exception('suitable only for Df1')
        stmt = self.get_select_for_Df1()
        obj: SQLModel = self.session.exec(stmt).scalar_one_or_none()
        if obj is None:
            self.session.add(self.row)
            return
        obj.SUM_NARAH += self.row.SUM_NARAH