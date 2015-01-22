import reedsolo

def _decode_block(dat, ecc, rs):
    dat = _decode_bin(dat)
    ecc = _decode_bin(ecc)
    dec = rs.decode(dat + ecc)
    return _encode_bin(dec)

def _decode_bin(s):
    n = []
    for i in range(0, len(s), 8):
        b = s[i:i+8]
        if '2' in b:
            n.append(0)
        else:
            n.append(int(b,2))
    b = map(chr, n)
    return bytearray(b)

def _encode_bin(b):
    return ''.join(map(lambda x: bin(x)[2:].zfill(8), b))

def correct_errors(dat, ecc):
    dat_len = len(dat[0]) // 8
    ecc_len = len(ecc[0]) // 8
    rs = reedsolo.RSCodec(ecc_len)

    block_cnt = len(dat)
    result = ["" for i in range(block_cnt)]
    for i in range(block_cnt):
        result[i] = _decode_block(dat[i], ecc[i], rs)
    return result

