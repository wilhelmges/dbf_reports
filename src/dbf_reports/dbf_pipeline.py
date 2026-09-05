import pathlib
from pathlib import Path
from sqlmodel import select, SQLModel

from dbf_reports.utils import get_file_hash, iterate_medok_folder
from dbf_reports.database.db import SessionFactory
from dbf_reports.database.filehash import FileHash
from dbf_reports.database.init_db import clear_tables

from dbf_reports.dbf.core import get_dbf_row_Class, is_df_report
from dbf_reports.dbf.process_rows import process_main, process_adjustments

import logging
from src.dbf_reports.config import setup_logging; setup_logging()
logger = logging.getLogger(__name__)

def dbf_pipeline(str_file_path, main=True):
    file = Path(str_file_path)
    if file.suffix != ".dbf" or not is_df_report(file):
        return False
    #print(is_dbf_already_imported(file))
    if is_dbf_already_imported(file):
        return True
    #Row_Processor = get_dbf_row_Class(file); print(Row_Processor)
    if main:
        rez = process_main(file)
    else:
        rez = process_adjustments(file)

    if rez:
        register_processed_dbf(file, main)
        return True
    else:
        return False

def is_dbf_already_imported(file: pathlib.Path):
    _hash = get_file_hash(file)
    with SessionFactory() as session:
        statement = select(FileHash).where(FileHash.hash == _hash)
        if session.exec(statement).first():
            return True
    return False

def register_processed_dbf(file: pathlib.Path, main:bool):
    with SessionFactory() as session:
        session.add(FileHash(hash=get_file_hash(file), filepath=str(file), main=main))
        session.commit()

if __name__ == "__main__":

    operations, adjustments, t = iterate_medok_folder("s:/МЕДОК")

    # print(len(operations))
    # clear_tables()
    # for op in operations:
    #     print(op)
    #     dbf_pipeline(op)

    print(len(adjustments))
    for aj in adjustments:
        rez = dbf_pipeline(aj, main=False)
        if not rez:
            print(aj, rez)
#filename = r'C:\progs\dbf reports\data\J0510106_2_23_1.dbf'