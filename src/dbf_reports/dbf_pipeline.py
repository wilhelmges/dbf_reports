import pathlib
from pathlib import Path
from sqlmodel import select, SQLModel



from utils import get_file_hash, iterate_medok_folder
from database.db import SessionFactory
from database.filehash import FileHash

from dbf.core import get_dbf_row_Class, is_df_report

from dbf.process_rows import process_main, process_adjustments #Table 'filehash' is already defined for this MetaData instance.
#print("Tables:", list(SQLModel.metadata.tables.keys())); exit(0)

import logging
from src.dbf_reports.config import setup_logging; setup_logging()
logger = logging.getLogger(__name__)

def dbf_pipeline(str_file_path, main=True):
    file = Path(str_file_path)
    if file.suffix != ".dbf" or not is_df_report(file):
        return False
    #print(is_dbf_already_imported(file))
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
    _hash = get_file_hash(file)
    with SessionFactory() as session:
        statement = select(FileHash).where(FileHash.hash == _hash)
        if session.exec(statement).first():
            return True
    return False

def register_processed_dbf(file: pathlib.Path):
    with SessionFactory() as session:
        session.add(FileHash(hash=get_file_hash(file), filepath=str(file)))
        session.commit()

if __name__ == "__main__":
    filename = r'C:\progs\dbf reports\data\J0510106_2_23_1.dbf'
    operations, adjustments, t = iterate_medok_folder("s:/МЕДОК")
    print(len(operations))
    for op in operations:
        #print(op)
        dbf_pipeline(op)

    # print(len(adjustments))
    # for aj in adjustments:
    #     print(aj)
    #     dbf_pipeline(aj, main=False)
exit(0)
# extrafields in s:\МЕДОК\2 кв. 2025\J0510510_Уточн 5 додаток_подати.dbf
# {'N16', 'N5', 'N10', 'N18', 'N8', 'N4', 'N15', 'N1', 'N7', 'N14', 'N', 'N6', 'N17', 'N9', 'N3', 'N13', 'N11'}
# extrafields in s:\МЕДОК\4 кв 2022\J0510406_3.dbf
# {'N17'}