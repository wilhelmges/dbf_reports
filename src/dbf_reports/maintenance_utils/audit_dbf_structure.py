from pathlib import Path
import pickle
from collections import defaultdict

from dbfread import DBF
from robust_dbfreader.dbf_reader import DbfRawFileReader

import src.dbf_reports.config
from src.dbf_reports.utils import iterate_medok_folder


def dbf_typed_fields(dbffile):
    table = DBF(f, load=False)
    fields = {}
    for field in table.fields:
        fields[field.name] = field.type
    return fields

def collect_field_types(structures: list[dict[str, str]]) -> dict[str, list[str]]:
    """
    Приймає список структур DBF-файлів та повертає словник:
        поле -> список усіх зустрінутих типів.

    Наприклад:
    [
        {"A": "C", "B": "N"},
        {"A": "C", "B": "D"},
        {"A": "N", "B": "N"},
    ]

    =>
    {
        "A": ["C", "N"],
        "B": ["D", "N"],
    }
    """
    field_types = defaultdict(set)

    for structure in structures:
        for field, field_type in structure.items():
            field_types[field].add(field_type)

    return {
        field: sorted(types)
        for field, types in field_types.items()
    }

if __name__ == "__main__":
    root = Path(config.config["main"]["DBF_START_DIR"])  # або Path(r"C:\my_folder")
    operations, adjustments, toresearch = iterate_medok_folder(root)
    print(len(operations), len(adjustments), len(toresearch))
    with open("operations.pkl", "wb") as f:
        pickle.dump(operations, f)
    with open("adjustments.pkl", "wb") as f:
        pickle.dump(adjustments, f)

    # structures = [dbf_typed_fields(str(f)) for f in operations]
    # print(structures)

    # f = (operations[0])
    # print(dbf_typed_fields(f))
    # structures = []
    # for f in operations:
    #     structures.append(dbf_typed_fields(f))
    # for f in adjustments:
    #     structures.append(dbf_typed_fields(f))
    # rez = collect_field_types(structures)
    # print(rez)


    # d = DbfRawFileReader(f)
    # for i in range(1, 3):
    #     print(d.iterate_fields(i))
    #
    # table = DBF(f, load=False)
    #
    # fields = {}
    # for field in table.fields:
    #     print(field.name, field.type)
    #     fields[field.name] = field.type
    # print(fields)

