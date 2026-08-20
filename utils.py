import re
from pathlib import Path
import hashlib


quarter_re = re.compile(
    r'^(?P<quarter>[1-4])\s+кв\.?\s+(?P<year>\d{4})$'
)
def is_quarter_folder(foldername:str)->bool:
    foldername = foldername.lower()
    # "кв" in folder.name.lower() and "202" in folder.name.lower()
    rez = quarter_re.match(foldername) is not None
    #print(foldername, rez)
    return rez

def dbf_report_params(filename):
    sway = filename.split("_")[0][-3]
    if sway.isdigit():
        return int(sway)
    return 0

def is_df_report(df: int|Path)->bool:
    if isinstance(df, Path):
        df = dbf_report_params(df.stem)
    if df == 1 or df == 4 or df == 5:
        return True
    return False

def iterate_medok_folder(str_file_path, needed_df_type=None):
    operations = []
    adjustments = []
    toresearch= []

    file_path = Path(str_file_path)
    for folder in file_path.iterdir():
        if folder.is_dir() and is_quarter_folder(folder.name):
            for file in folder.glob("*.dbf"):
                dfnum = dbf_report_params(file.stem)
                if (file.stem.lower().startswith("j") and
                        is_df_report(dfnum)) \
                        and (not needed_df_type or dfnum == needed_df_type):
                    operations.append(file)
                else:
                    toresearch.append(file)

            for adjfolder in folder.iterdir():
                if adjfolder.is_dir() and "уточнен" in adjfolder.name.lower():# перевірка без врахування регістру
                    for file in adjfolder.glob("*.dbf"):
                        dfnum = dbf_report_params(file.stem)
                        if file.stem.lower().startswith("j") and is_df_report(dfnum) and (not needed_df_type or dfnum == needed_df_type):
                            adjustments.append(file) #pass
                        else:
                            toresearch.append(file)

    return operations, adjustments, toresearch

def file_hash(file: Path|str) -> str:
    if isinstance(file, str):
        file = Path(file)
    sha256 = hashlib.sha256()
    with file.open("rb") as f:
        while chunk := f.read(1024 * 1024):  # 1 MB
            sha256.update(chunk)
    return sha256.hexdigest()

if __name__=='__main__':
    pass #print(is_quarter_folder("3 кв 2025"))