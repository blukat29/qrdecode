import os
from codec import *
from decoder import *
from ec import *

def run_case(raw):
    ver, arr = to_arr(raw)
    ec_level, mask_id = read_format(arr, strict=False)
    arr = mask(ver, arr, mask_id)
    words = walk(ver, arr)
    dat, ecc = split_blocks(ver, ec_level, words)
    dat = correct_errors(dat, ecc)
    res = QRCodec.decode(ver, dat)
    return res


for root, dirs, files in os.walk("tests/"):
    for name in files:
        f = open(os.path.join(root, name))
        raw = ""
        for line in f.readlines():
            if not line.startswith(";"):
                raw += line
        f.close()
        print "[[ %s ]]" % name
        print run_case(raw)

