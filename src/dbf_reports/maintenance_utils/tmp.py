strfile = r's:/МЕДОК/3 кв. 2022/Уточнення/J0510506.dbf'

def get_quarter_folder(strfile):
    print (strfile.split('/')[2])

def encoded_quarter(strfile):
    s = (strfile.split('\\')[2])
    sn = (s[-4:]+ s[:1])
    return (int(sn))

(get_quarter_folder(strfile))
# a = [""] * 5001
# a[7]="ggg"; a[4000]="rgr"
# result = [s for s in a if s]
# print(result)