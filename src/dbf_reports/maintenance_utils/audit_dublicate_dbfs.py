import pickle
import hashlib
from pathlib import Path
from collections import Counter

def file_hash(path: Path|str):
    h = hashlib.blake2b()
    with path.open("rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()

if __name__=="__main__":
    with open("operations.pkl", "rb") as f:
        operations = pickle.load(f)
    with open("adjustments.pkl", "rb") as f:
        adjustments = pickle.load(f)
    dbfs = operations+adjustments
    sf = [str(f) for f in dbfs]
    file_hashes = {f: file_hash(f) for f in dbfs}

    counts = Counter(file_hashes.values())
    result = {
        key: value[:10]
        for key, value in file_hashes.items()
        if counts[value] > 1
    }
    print(result)

    # hashes = [file_hash(f) for f in dbfs]
    # print(len(hashes))
    # print(len(set(hashes)))
    #
    # print(len(sf))
    # print(len(set(sf)))

