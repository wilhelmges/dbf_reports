my_dict = {
    "name": "John",
    "age": 25,
    "age2": 45,
    "city2": "Kyiv"
}


def remove2inkeys(rec):
    neorec = {}
    for key, value in rec.items():
        print(key, value)
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


rec = remove2inkeys(my_dict)
print(rec)

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
