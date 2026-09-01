import datetime

value = '02.01.23'
print(repr(value))
print(datetime.datetime.strptime(value, '%d.%m.%y').date())


# from typing import get_args
#
# x = int | str
# print(type(x))
# print(get_args(x)[0])
# print(get_args(x)[0].__name__)
# <class 'types.UnionType'>
# table = DBF("data/J0510106_1_23_1.dbf", encoding="cp866")  # або cp1251, якщо потрібно
#
# for row in table:
#     print(row)
#     break