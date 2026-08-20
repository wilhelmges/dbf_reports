import pathlib
from pathlib import Path
from sqlmodel import select

from utils import dbf_report_params, file_hash
from database.db import session
from database.models import FileHash

def process_file(str_file_path, main=False):
    file = Path(str_file_path)
    print(canbe_imported(file))
    if not canbe_imported(file):
        return False

    dbftype = dbf_report_params(file.stem)
    print(dbftype)

def canbe_imported(file: pathlib.Path):
    if file.suffix != ".dbf":
        return False
    _hash = file_hash(file)
    with session:
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
