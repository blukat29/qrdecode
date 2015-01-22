import sys
sys.path.insert(0, "..")
from decoder import *
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
ec_level, mask_id =  read_format(arr, strict=True)
arr = mask(ver, arr, mask_id)
words = walk(ver, arr)
dat, ecc = split_blocks(ver, ec_level, words)
print dat
print ecc
dat = ''.join(dat)
print QRCodec.decode(ver, dat)

