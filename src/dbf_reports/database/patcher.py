from sqlmodel import Session

from dbf_reports.database.dfmodels import Df1, Df4, Df5
from dbf_reports.database.dfmodel_repository import Repository

import logging
from src.dbf_reports.config import setup_logging; setup_logging()
logger = logging.getLogger(__name__)

class AdjustmentCantBePatchedException(Exception):
    pass

def apply_row_from_adjustment(row_for_search, session: Session):

    if isinstance(row_for_search, Df1):
        r = Repository(session, Df1)
        statement = r.find_statement_by_key(row_for_search)
        if row_for_search.PAY_TP == 2:
            df = session.exec(statement).one_or_none()
            if df:
                df.SUM_NARAH += row_for_search.SUM_NARAH
        elif row_for_search.PAY_TP == 3:
            df = session.exec(statement).one()
            df.SUM_NARAH -= row_for_search.SUM_NARAH
            if df.SUM_NARAH < 0.1:
                session.delete(df)
        elif row_for_search.OZN == 1:
            #c = r.count_by_key(row_for_search); print(f'rows kith keyfields {c}')
            df = session.exec(statement).one()
            session.delete(df)
        elif row_for_search.OZN == 0:
            session.add(row_for_search)
        else:
            raise AdjustmentCantBePatchedException('indefinite operation')

    elif isinstance(row_for_search, Df4):
        pass
    elif isinstance(row_for_search, Df5):
        pass
    else:
        pass