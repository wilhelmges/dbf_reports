import pathlib
from pathlib import Path
from sqlmodel import select
from utils import file_hash, iterate_medok_folder
from database.db import SessionFactory
from database.models import FileHash
from dbf.core import get_dbf_row_Class, is_df_report
from dbf.process_rows import process_main, process_adjustments


import logging
from src.dbf_reports.config import setup_logging; setup_logging()
logger = logging.getLogger(__name__)

def dbf_pipeline(str_file_path, main=False):
    file = Path(str_file_path)
    if file.suffix != ".dbf" or not is_df_report(file):
        return False
    print(is_dbf_already_imported(file))
    if is_dbf_already_imported(file):
        return False
    #Row_Processor = get_dbf_row_Class(file); print(Row_Processor)
    if main:
        rez = process_main(file)
    else:
        rez = process_adjustments(file)
    if rez:
        register_processed_dbf(file)
        return True

def is_dbf_already_imported(file: pathlib.Path):
    _hash = file_hash(file)
    with SessionFactory() as session:
        statement = select(FileHash).where(FileHash.hash == _hash)
        if session.exec(statement).first():
            return True
    return False

def register_processed_dbf(file: pathlib.Path):
    with SessionFactory() as session:
        session.add(FileHash(hash=file_hash(file), filepath=str(file)))


if __name__ == "__main__":
    filename = r'C:\progs\dbf reports\data\J0510106_2_23_1.dbf'
    dbf_pipeline(filename)
