
from tables import *

def dump_arr(a, conv, fancy=False):
    s = ""
    if fancy:
        s += " "
        for i in range(len(a)):
            s += " %d" % (i % 10)
        s += "\n"

    for i in range(len(a)):
        if fancy:
            s += "%d " % (i % 10)
        for j in range(len(a[i])):
            k = a[i][j]
            if k not in conv:
                s += k + " "
            else:
                s += conv[a[i][j]] + " "
        s += "\n"
    return s


def to_arr(s):
    """
    Convert multi-line string to 2d array.
    Use 'XxOo#1' for white, '_-0. ' for black, '?~' for wildcard.
    Input must be square of size (4k + 17) with k = 1,2,3,...,40.
    """
    lines = filter(None, s.split("\n"))

    N = len(lines)
    if N not in range(21, 178, 4):
        raise ValueError("Bad dimension")
    dat = [[0]*N for i in range(N)]

    for i in range(N):
        if N != len(lines[i]):
            raise ValueError("Input not square")
        for j in range(N):
            c = lines[i][j]
            if c in "XxOo#1":  dat[i][j] = 1
            elif c in "_-0. ": dat[i][j] = 0
            elif c in "?~":    dat[i][j] = 2
            else: raise ValueError("invalid char '%s'" % c)

    ver = (N - 17) / 4
    return ver, dat


def _hamming_distance(n, s):
    """
    Hamming distance between {0,1,2}^k and {"0","1"}^k.
    Distance between 2 and anything is 1.
    """
    dist = 0
    for i in range(min(len(n), len(s))):
        if n[i] != int(s[i]):
            dist += 1
    dist += abs(len(n) - len(s))
    return dist


def read_format(arr, strict=False):
    """
    The array must be the one before unmasking.
    Extract format string from full array and interpret it.
    Recover possible error. Returns (ec_level, mask_id)
    """
    # Extract raw bits
    horz_idxes = [0,1,2,3,4,5,7] + [-8,-7,-6,-5,-4,-3,-2,-1]
    horz_fs = map(lambda i: arr[8][i], horz_idxes)
    vert_idxes = [-1,-2,-3,-4,-5,-6,-7] + [8,7] + [5,4,3,2,1,0]
    vert_fs = map(lambda i: arr[i][8], vert_idxes)

    max_dist = 100
    horz_idx = -1
    vert_idx = -1
    for i, s in enumerate(format_string_table):
        d = _hamming_distance(horz_fs, s)
        if d < max_dist:
            if not strict or d <= 3:
                max_dist = d
                horz_idx = i
        d = _hamming_distance(vert_fs, s)
        if d < max_dist:
            if not strict or d <= 3:
                max_dist = d
                vert_idx = i

    if horz_idx == -1 and vert_idx == -1:
        raise ValueError("Cannot decode format string")
    elif horz_idx == -1:
        return vert_idx // 8, vert_idx % 8
    elif vert_idx == -1:
        return horz_idx // 8, horz_idx % 8
    elif horz_idx == vert_idx:
        return horz_idx // 8, horz_idx % 8
    else:
        raise ValueError("Two format strings disagree")


def mask(ver, arr, mask_id):

    if mask_id not in range(8):
        raise ValueError("Bad mask id")

    mask_list = [
        (lambda i,j: (i+j) % 2 == 0),
        (lambda i,j: i % 2 == 0),
        (lambda i,j: j % 3 == 0),
        (lambda i,j: (i+j) % 3 == 0),
        (lambda i,j: (i//2 + j//3) % 2 == 0),
        (lambda i,j: ((i*j) % 2 + (i*j) % 3) == 0),
        (lambda i,j: ((i*j) % 3 + i*j) % 2 == 0),
        (lambda i,j: ((i*j) % 3 + i + j) % 2 == 0)
    ]
    mask_func = mask_list[mask_id]

    N = ver * 4 + 17
    for i in range(N):
        for j in range(N):
            if mask_func(i,j):
                arr[i][j] = {0:1, 1:0, 2:2}[arr[i][j]]

    return arr


def _mark_reserved(ver):
    N = ver * 4 + 17
    r = [[False]*N for i in range(N)]

    # Finder patterns
    for x in range(9):
        for y in range(9):
            r[x][y] = True

    for x in range(N-8, N):
        for y in range(9):
            r[x][y] = True

    for x in range(9):
        for y in range(N-8, N):
            r[x][y] = True

    # Timing patterns
    for i in range(N):
        r[6][i] = True
        r[i][6] = True

    # Alignment patterns
    table = alignment_pattern_table[ver]
    for x in table:
        for y in table:
            # Skip around finder patterns
            if x < 9 and y < 9: continue
            if N-10 < x and y < 9: continue
            if x < 9 and N-10 < y: continue

            for dx in [-2,-1,0,1,2]:
                for dy in [-2,-1,0,1,2]:
                    r[x+dx][y+dy] = True

    # Version information
    if ver >= 7:
        for i in range(3):
            for j in range(6):
                r[N-11+i][j] = True
                r[i][N-11+j] = True

    return r


def walk(ver, arr):
    N = ver * 4 + 17
    r = _mark_reserved(ver)
    # print dump_arr(r, {True:'+', False:'-'}, True)

    x = N-1
    y = N-1
    words = []
    word = ""

    while True:
        if x < 0 or y < 0:
            break

        # Harvest non-reserved module
        if r[y][x] == False:
            word += str(arr[y][x])
            if len(word) == 8:
                words.append(word)
                word = ""

        # Consider left timing pattern
        if x < 7: tx = x
        else: tx = x - 1

        # Zig-zag
        if tx % 2 == 1:
            x -= 1
        else:
            if (tx // 2) % 2 == 1:  # Up
                if y == 0:
                    x -= 1
                else:
                    y -= 1
                    x += 1
            else:  # Down
                if y == N-1:
                    if (tx // 2) == 3:  # Skip left timing pattern
                        x -= 1
                    x -= 1
                else:
                    y += 1
                    x += 1

    return words


def split_blocks(ver, ec_level, words):
    ecc_per_block = ecc_length_table[ver][ec_level]
    block_size = block_size_table[ver][ec_level]

    block_count = block_size[0]
    data_count = block_size[0] * block_size[1]
    if len(block_size) > 2:
        block_count += block_size[2]
        data_count += block_size[2] * block_size[3]
    ecc_count = block_count * ecc_per_block

    data_blocks = ["" for i in range(block_count)]
    for i in range(data_count):
        data_blocks[i % block_count] += words[i]

    words = words[data_count:]
    ecc_blocks = ["" for i in range(block_count)]
    for i in range(ecc_count):
        ecc_blocks[i % block_count] += words[i]

    return ''.join(data_blocks), ''.join(ecc_blocks)

