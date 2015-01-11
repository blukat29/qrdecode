
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
    table = _alignment_pattern_table[ver]
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


_alignment_pattern_table = [
    [],
    [],
    [6, 18],
    [6, 22],
    [6, 26],
    [6, 30],
    [6, 34],
    [6, 22, 38],
    [6, 24, 42],
    [6, 26, 46],
    [6, 28, 50],
    [6, 30, 54],
    [6, 32, 58],
    [6, 34, 62],
    [6, 26, 46, 66],
    [6, 26, 48, 70],
    [6, 26, 50, 74],
    [6, 30, 54, 78],
    [6, 30, 56, 82],
    [6, 30, 58, 86],
    [6, 34, 62, 90],
    [6, 28, 50, 72, 94],
    [6, 26, 50, 74, 98],
    [6, 30, 54, 78, 102],
    [6, 28, 54, 80, 106],
    [6, 32, 58, 84, 110],
    [6, 30, 58, 86, 114],
    [6, 34, 62, 90, 118],
    [6, 26, 50, 74, 98, 122],
    [6, 30, 54, 78, 102, 126],
    [6, 26, 52, 78, 104, 130],
    [6, 30, 56, 82, 108, 134],
    [6, 34, 60, 86, 112, 138],
    [6, 30, 58, 86, 114, 142],
    [6, 34, 62, 90, 118, 146],
    [6, 30, 54, 78, 102, 126, 150],
    [6, 24, 50, 76, 102, 128, 154],
    [6, 28, 54, 80, 106, 132, 158],
    [6, 32, 58, 84, 110, 136, 162],
    [6, 26, 54, 82, 110, 138, 166],
    [6, 30, 58, 86, 114, 142, 170]
]

