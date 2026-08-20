import pathlib
from pathlib import Path
from sqlmodel import select
from dbf.core import dbf_report_params
from utils import file_hash
from database.db import session
from database.db import SessionFactory
from database.models import FileHash
from dbf.core import get_dbf_row_Class, is_df_report

def process_file(str_file_path, main=False):
    file = Path(str_file_path)
    print(canbe_imported(file))
    if not canbe_imported(file):
        return False
    if not is_df_report(file):
        return False
    Row_Processor = get_dbf_row_Class(file)
    print(Row_Processor)

def canbe_imported(file: pathlib.Path):
    if file.suffix != ".dbf":
        return False
    _hash = file_hash(file)
    with SessionFactory() as session:
        statement = select(FileHash).where(FileHash.hash == _hash)
        h = session.exec(statement).first()
        if h:
            return False
    return True

def register_processed_dbf(file: pathlib.Path):
    with session:
        session.add(FileHash(hash=file_hash(file), filepath=str(file)))


if __name__ == "__main__":
    filename = r'C:\progs\dbf reports\data\J0510106_2_23_1.dbf'
    process_file(filename)
