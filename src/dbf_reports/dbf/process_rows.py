from pathlib import Path
from pydantic import ValidationError
from robust_dbfreader.dbf_reader import DbfRawFileReader
from sqlmodel import SQLModel, case
from sqlalchemy import Float

from dbf_reports.database.db import SessionFactory
from dbf_reports.database.dfmodels import Df1, Df4, Df5
from dbf_reports.utils import normalize_ukrainian_text
from dbf_reports.dbf.unbreaker import get_from_broken_value
from dbf_reports.dbf.core import dbf_report_params
from dbf_reports.database.adjustment_service import apply_row_from_adjustment, CantApplyRowException

import logging
from dbf_reports.config import setup_logging;
setup_logging()
logger = logging.getLogger(__name__)
import traceback


def normalize_adjustment_rec(rec):
    raise Exception('not implemented')


def get_model_from_file(file):
    typenum = dbf_report_params(file)
    match typenum:
        case 1:
            return Df1
        case 4:
            return Df4
        case 5:
            return Df5
        case _:
            raise Exception('Wrong model type')


class FieldCantbeConverted(Exception):
    pass

def remove2inkeys(rec):
    neorec = {}
    for key, value in rec.items():
        neokey = key
        if key.endswith("2"):
            if (value is not None) and (value != ""):
                neokey = key[:-1]
                neorec[neokey] = value
        else:
            neorec[key] = value
    return neorec
    my_dict = {'NP': 1618.0, 'PERIOD': '9', 'RIK': 2024.0, 'KOD': '', 'TYP': 0.0, 'TIN': '2780704342',
               'S_NAR': 32119.67, 'S_DOX': 32119.67, 'S_TAXN': 5781.54, 'S_TAXP': 5781.54, 'OZN_DOX': 185.0,
               'D_PRIYN': '', 'D_ZVILN': '', 'OZN_PILG': '', 'OZNAKA': '', 'A051': '479,84', 'A05': '479,84',
               'D_ZVILN2': '', 'OZN_PILG2': '', 'OZNAKA2': '1'}

def normalize_rec_for_model(rec, df_model: type[SQLModel]):
    if df_model is Df1 or df_model is Df5:
        rec['LN'] = normalize_ukrainian_text(rec['LN']).lower()
        rec['NM'] = normalize_ukrainian_text(rec['NM']).lower()
        rec['FTN'] = normalize_ukrainian_text(rec['FTN']).lower()
    elif df_model is Df4:
        return rec
    else:
        raise Exception('Wrong model type')
    return rec

ignore_fields = ['id', 'SYS_ERROR']
def get_row(rec, df_model: type[SQLModel]):
    cleared_data = {}
    rec = normalize_rec_for_model(rec, df_model)
    for field_name, field_info in df_model.model_fields.items():
        if field_name in ignore_fields:
            continue
        raw_value = rec.get(field_name)
        if raw_value is None or raw_value == '':
            cleared_data[field_name] = None
            continue
        # Використовуємо внутрішній валідатор Pydantic для конкретного поля
        # Це спробує перетворити тип (наприклад, рядок "123" у int)
        try:
            validated_value = df_model.model_validate(
                {field_name: raw_value},
                from_attributes=True
            )
            value = getattr(validated_value, field_name)
        except ValidationError as e:
            value = get_from_broken_value(raw_value, field_info.annotation)
            # print(f' value after fix {value}')
        cleared_data[field_name] = value
    return df_model(**cleared_data)

def process_main(file) -> bool:
    """returns True if processed successfully"""
    d = DbfRawFileReader(file)
    df_model = get_model_from_file(file)
    rec = remove2inkeys(d.read_record(1))
    dict_fields = set(rec.keys())
    model_fields = set(df_model.model_fields.keys())
    diff = dict_fields - model_fields
    if diff:
        print(f'extrafields in {file}')
        print(diff)
        return False

    with SessionFactory() as session:
        with session.begin():
            for i in range(1, d.recordnum):
                rec = remove2inkeys (d.read_record(i))
                row = get_row(rec, df_model)
                session.add(row)
    return True


def process_adjustments(file: Path):
    d = DbfRawFileReader(file)
    df_model = get_model_from_file(file)
    rec = remove2inkeys(d.read_record(1))
    dict_fields = set(rec.keys())
    model_fields = set(df_model.model_fields.keys())
    diff = dict_fields - model_fields
    if diff:
        print(f'extrafields in {file} {diff}')
        print(diff)
        logger.warning(f'extrafields {diff} in {file} ')
        return False

    with SessionFactory() as session:
        with session.begin():
            for i in range(1, d.recordnum):
                rec = remove2inkeys(d.read_record(i))
                rec = normalize_rec_for_model(rec, df_model)
                row = get_row(rec, df_model)
                try:
                    apply_row_from_adjustment(row, session)
                except CantApplyRowException as e:
                    print(f'cant patch row {i} in {file}')
                    print(row.LN, row.PAY_TP, row.OZN)
                    logger.warning(f'cant patch row {i} in {file}')
                    logger.warning(str(e))
                    session.rollback()
                    return False

                except Exception as e:
                    logger.warning(f'unknown in row {i}  {file}')
                    session.rollback()
                    return False


    session.commit()
    return True





# {'NP': 1618.0, 'PERIOD': '9', 'RIK': 2024.0, 'KOD': '', 'TYP': 0.0, 'TIN': '2780704342', 'S_NAR': 32119.67, 'S_DOX': 32119.67, 'S_TAXN': 5781.54, 'S_TAXP': 5781.54, 'OZN_DOX': 185.0, 'D_PRIYN': '', 'D_ZVILN': '', 'OZN_PILG': '', 'OZNAKA': '', 'A051': '479,84', 'A05': '479,84', 'D_ZVILN2': '', 'OZN_PILG2': '', 'OZNAKA2': '1'}


if __name__ == "__main__":
    # _ = get_row(rec, Df1); print(_); exit(0)
    # cant patch row 3 in
    file = r's:\МЕДОК\2 кв. 2023\Уточнення Царук Віталій Адамович\J0510106_Царук ВА_Редзель СМ_6.dbf'
    #file = r's:\МЕДОК\3 кв. 2024\Уточнення_ПОМЯЛОВ_9_2024\J0510409_3.dbf'
    process_adjustments(Path(file))

    exit(0)
    d = DbfRawFileReader(file)
    print(d.read_record(5110))
    print(d.read_record(5111))
    # rec = {'PERIOD_M': 2.0, 'PERIOD_Y': 2023.0, 'UKR_GROMAD': 1.0, 'ST': 1.0, 'NUMIDENT': '2765411390', 'LN': 'ХОБТА', 'NM': 'СЕРГІЙ', 'FTN': 'Іванович', 'ZO': 51.0, 'PAY_TP': '', 'PAY_MNTH': 2.0, 'PAY_YEAR': 2023.0, 'KD_NP': '', 'KD_NZP': '', 'KD_PTV': 28.0, 'KD_VP': '', 'SUM_TOTAL': 26555.84, 'SUM_MAX': 26555.84, 'SUM_DIFF': '', 'SUM_INS': '', 'SUM_NARAH': 5842.28, 'OTK': '', 'EXP': '', 'NRC': '', 'NRM': '', 'OZN': ''}
