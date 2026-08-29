from pathlib import Path
import dbf
from pyasn1.type.univ import Boolean
from pydantic import ValidationError
from robust_dbfreader.dbf_reader import DbfRawFileReader
from sqlmodel import SQLModel
from src.dbf_reports.database.db import SessionFactory
from src.dbf_reports.database.models import Df1, Df4, Df5
from src.dbf_reports.utils import normalize_ukrainian_text

import logging
from src.dbf_reports.config import setup_logging; setup_logging()
logger = logging.getLogger(__name__)


class FieldCantbeConverted(Exception):
    pass

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

ignore_fields = ['id','SYS_ERROR']
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
        try:
            # Використовуємо внутрішній валідатор Pydantic для конкретного поля
            # Це спробує перетворити тип (наприклад, рядок "123" у int)
            validated_value = df_model.model_validate(
                {field_name: raw_value},
                from_attributes=True
            )
            cleared_data[field_name] = getattr(validated_value, field_name)
        except (ValidationError, ValueError, TypeError) as e:
            # Якщо перетворення неможливе
            logger.warning(
                f"Попередження: Не вдалося конвертувати поле '{field_name}' "
                f"зі значенням '{raw_value}' до типу {field_info.annotation}. "
                f"Встановлюється значення None. Помилка: {e}"
            )
            cleared_data[field_name] = None
            raise FieldCantbeConverted('one of field cant be converted')

    return df_model(**cleared_data)

def process_main(file:Path)->Boolean:
    """returns True if processed successfully"""
    d = DbfRawFileReader(file)
    model = Df1
    rec = d.read_record(1)
    dict_fields = set(rec.keys())
    model_fields = set(Df1.model_fields.keys())
    if dict_fields-model_fields:
        return False
    with SessionFactory() as session:
        with session.begin():
            for i in range(1,d.recordnum):
                rec = d.read_record(i)
                raw = get_row(rec, model)
                session.add(raw)
    return True


def process_adjustments(file:Path):
    return False

if __name__ == "__main__":
    # _ = get_row(rec, Df1); print(_); exit(0)
    file = r'C:\progs\dbf reports\data\J0510106_2_23_1.dbf'
    process_main(Path(file))


    #rec = {'PERIOD_M': 2.0, 'PERIOD_Y': 2023.0, 'UKR_GROMAD': 1.0, 'ST': 1.0, 'NUMIDENT': '2765411390', 'LN': 'ХОБТА', 'NM': 'СЕРГІЙ', 'FTN': 'Іванович', 'ZO': 51.0, 'PAY_TP': '', 'PAY_MNTH': 2.0, 'PAY_YEAR': 2023.0, 'KD_NP': '', 'KD_NZP': '', 'KD_PTV': 28.0, 'KD_VP': '', 'SUM_TOTAL': 26555.84, 'SUM_MAX': 26555.84, 'SUM_DIFF': '', 'SUM_INS': '', 'SUM_NARAH': 5842.28, 'OTK': '', 'EXP': '', 'NRC': '', 'NRM': '', 'OZN': ''}