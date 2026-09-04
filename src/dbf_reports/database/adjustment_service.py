from sqlmodel import Session

from dbf_reports.database.dfmodels import Df1, Df4, Df5
from dbf_reports.database.dfmodel_repository import Repository

import logging
# from src.dbf_reports.config import setup_logging; setup_logging()
logger = logging.getLogger(__name__)

class CantApplyRowException(Exception):
    pass

def apply_row_from_adjustment(row, session: Session):

    if isinstance(row, Df1):
        r = Repository(session, Df1)
        statement = r.find_statement_by_key(row)
        if row.PAY_TP == 2:
            df = session.exec(statement).one_or_none()
            if df:
                df.SUM_NARAH += row.SUM_NARAH
        elif row.PAY_TP == 3:
            df = session.exec(statement).one()
            df.SUM_NARAH -= row.SUM_NARAH
            if df.SUM_NARAH < 0.1:
                session.delete(df)
        elif row.OZN == 1:
            try:
                df = session.exec(statement).one()
                session.delete(df)
            except Exception as e:
                c = r.count_by_key(row); print(f'rows kith keyfields {c}')
                print(str(e))
                raise CantApplyRowException(f'cant patch {row.LN},{row.PAY_TP},{row.OZN} rows kith keyfields {c}')
        elif row.OZN == 0:
            session.add(row)
        else:
            raise CantApplyRowException(f'df1 indefinite operation for {row.LN},{row.PAY_TP},{row.OZN}')


    elif isinstance(row, Df4):
        r = Repository(session, Df4)
        statement = r.find_statement_by_key(row)
        if row.OZN == 1:
            df = session.exec(statement).one()
            session.delete(df)
        elif row.OZN == 0:
            session.add(row)
        else:
            raise CantApplyRowException(f'df4 indefinite operation for {row.LN}, {row.OZN}')


    elif isinstance(row, Df5):
        r = Repository(session, Df5)
        statement = r.find_statement_by_key(row)
        if row.OZN == 1:
            df = session.exec(statement).one()
            session.delete(df)
        elif row.OZN == 0:
            session.add(row)
        else:
            raise CantApplyRowException(f'df5 indefinite operation for {row.LN}, {row.OZN}')

    else:
        raise CantApplyRowException(f'indefenite df model')