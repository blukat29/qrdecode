import os
from codec import *
from decoder import *
from ec import *
from img import *

def run_case(raw):
    ver, arr = to_arr(raw)
    ec_level, mask_id = read_format(arr, strict=False)
    arr = mask(ver, arr, mask_id)
    words = walk(ver, arr)
    dat, ecc = split_blocks(ver, ec_level, words)
    dat = correct_errors(dat, ecc)
    res = QRCodec.decode(ver, dat)
    return res

def test_text(path):
    f = open(path)
    raw = ""
    for line in f.readlines():
        if not line.startswith(";"):
            raw += line
    f.close()
    return run_case(raw)

def test_img(path):
    raw = detect(path)
    return run_case(raw)

for root, dirs, files in os.walk("tests/"):
    for name in files:
        path = os.path.join(root, name)
        print "[[ %s ]]" % name
        if name.endswith("txt"):
            print test_text(path)
        else:
            print test_img(path)

