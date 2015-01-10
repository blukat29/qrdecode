
def panic(msg):
    print msg
    exit(1)

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

class QRDecoder:

    def __init__(self, s, error_level="H", mask_id=1):
        self.d = QRDecoder.to_arr(s)
        self.N = len(self.d)
        self.ver = QRDecoder.dim_to_ver(self.N)

        self.error_level = error_level
        self.mask_id = mask_id

    def decode(self):
        self.is_reserved = self.mark_reserved()
        self.d = self.unmask(self.mask_id)
        self.b = self.walk()
        # skip error correction

    @staticmethod
    def dim_to_ver(N):
        if (N - 21) % 4 != 0 or N < 21 or 177 < N:
            panic("bad dimension")
        return (N - 21) // 4 + 1

    @staticmethod
    def to_arr(s):
        lines = filter(None, s.split("\n"))

        N = len(lines)
        dat = [[0]*N for i in range(N)]

        for i in range(N):
            assert(N == len(lines[i]) and "input is square")
            for j in range(N):
                c = lines[i][j]
                if c in "XxOo#1": dat[i][j] = 1
                elif c in "_-0 .": dat[i][j] = 0
                elif c in "?~": dat[i][j] = 2
                else: panic("Unknown char")

        return dat

    def dump(self, fancy=False):
        return dump_arr(self.d, {0:"-", 1:"X", 2:"?"}, fancy)

    def unmask(self, mask_id=0):

        if mask_id not in range(8): panic("Unknown mask id")

        masks = [
            (lambda i,j: (i+j) % 2 == 0),
            (lambda i,j: i % 2 == 0),
            (lambda i,j: j % 3 == 0),
            (lambda i,j: (i+j) % 3 == 0),
            (lambda i,j: (i//2 + j//3) % 2 == 0),
            (lambda i,j: ((i*j) % 2 + (i*j) % 3) == 0),
            (lambda i,j: ((i*j) % 3 + i*j) % 2 == 0),
            (lambda i,j: ((i*j) % 3 + i + j) % 2 == 0)
        ]
        mask = masks[mask_id]

        d = self.d
        N = self.N
        for i in range(N):
            for j in range(N):
                if mask(i,j):
                    c = d[i][j]
                    d[i][j] = {0:1, 1:0, 2:2}[c]

        return d

    def mark_reserved(self):
        """
        http://www.thonky.com/qr-code-tutorial/module-placement-matrix/
        """
        N = self.N
        r = [[False]*N for i in range(N)]

        # Finder patterns
        for x in range(9):
            for y in range(9):
                r[x][y] = 'F'

        for x in range(N-8, N):
            for y in range(9):
                r[x][y] = 'F'

        for x in range(9):
            for y in range(N-8, N):
                r[x][y] = 'F'

        # Timing patterns
        for i in range(N):
            r[6][i] = 'T'
            r[i][6] = 'T'

        # Alignment patterns
        tab = QRDecoder.align_pattern_table[self.ver]
        for x in tab:
            for y in tab:
                if (x < 9 and y < 9): continue    # Left top
                if (N-10 < x and y < 9): continue # Left bottom
                if (x < 9 and N-10 < y): continue # Right top

                for dx in range(-2,3):
                    for dy in range(-2,3):
                        r[x+dx][y+dy] = 'A'

        # Version information
        if self.ver >= 7:
            for i in range(3):
                for j in range(6):
                    r[N-11+i][j] = 0
                    r[i][N-11+j] = 0
        return r

    def walk(self):
        d = self.d
        N = self.N
        r = self.is_reserved

        x = N-1
        y = N-1
        j = 0
        words = []
        word = ""
        while True:

            if x < 0 or y < 0:
                break

            if r[y][x] == False:
                word += str(d[y][x])
                j += 1
                if j == 8:
                    j = 0
                    words.append(word)
                    word = ""

            # To consider left timing pattern
            if x < 7: tx = x
            else: tx = x - 1

            # Exercise zig-zag move
            if tx % 2 == 1:  # right side of a block
                x -= 1
            else:            # left side of a block
                if (tx // 2) % 2 == 1:  # up
                    if y == 0:      # top reached
                        x -= 1
                    else:
                        y -= 1
                        x += 1
                else:                    # down
                    if y == N-1:    # bottom reached
                        if (tx // 2) == 3:  # skip left timing pattern
                            x -= 1
                        x -= 1
                    else:
                        y += 1
                        x += 1

        return words

    #---- Constant tables ------------------------------#

    # http://www.thonky.com/qr-code-tutorial/alignment-pattern-locations/
    align_pattern_table = [
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

