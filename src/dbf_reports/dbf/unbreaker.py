from typing import get_args
from datetime import datetime


def get_from_broken_value(broken_value, type_annotation: str):
    args = get_args(type_annotation)
    if args:
        strtype = args[0].__name__
    else:
        strtype = type_annotation.__name__
    # print(f'broken value {broken_value} -> {type_annotation}')
    if strtype == 'float':
        broken_value = ''.join(broken_value.split()).replace(',', '.')
        return float(broken_value)
    if strtype == 'date':
        broken_value = broken_value.replace('/', '.')
        if len(broken_value)==10:
            return datetime.strptime(broken_value, '%d.%m.%Y').date()
        if len(broken_value)==8:
            return datetime.strptime(broken_value, '%d.%m.%y').date()
    else:
        raise Exception(f'dont know how to fix {broken_value} to {type_annotation}')

    return None
