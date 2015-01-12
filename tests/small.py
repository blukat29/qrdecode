import sys
sys.path.insert(0, "..")
from new import *
from codec import *

s = """
#######...##..#######
#.....#.#...#.#.....#
#.###.#.#...#.#.###.#
#.###.#.#...#.#.###.#
#.###.#.#.###.#.###.#
#.....#.#.#...#.....#
#######.#.#.#.#######
.....................
..#..#######.#.#####.
...###.######.#..#..#
##.##.##..#.#.#...#.#
.###....#..#.#..##..#
###...##..####......#
........##..##.#...#.
#######.######.###..#
#.....#.##..#.##.....
#.###.#...#..#.##...#
#.###.#....####......
#.###.#.##...##...###
#.....#..##.#.#.#....
#######...##..#..##.#
"""

ver, arr = to_arr(s)
arr = mask(ver, arr, 1)
words = walk(ver, arr)
w = ''.join(words[:9])
print QRCodec.decode(ver, w)


