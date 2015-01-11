import sys, os
sys.path.insert(0, "..")
from new import *

# SECCON CTF Quals 2014 winter
# "QR_Easy"
raw = """
?????????????????x    xxxxxxx
????????????????? xxx x     x
?????????????????x xx x xxx x
????????????????? x   x xxx x
?????????????????xx x x xxx x
????????????????? x x x     x
????????????????? x x xxxxxxx
????????????????? x x        
??????????????????x xx xxxxx 
?????????????????x x x x    x
???????????????????x x  xxxx 
???????????????????    xxxxxx
?????????????????? x   xxx   
??????????????????  x xx x x 
??????????????????   xxxxxxx 
??????????????????  xx   x x 
??????????????????  xx x  x x
???????????????????xxx   x   
??????????????????? x   x x x
??????????????????   x  x  xx
?????????????????? xxxxxx xxx
??????????????????  x   x   x
???????????????????xx x x x  
???????????????????xx   x    
???????????????????xxxxxx x x
?????????????????? x x x xx  
??????????????????xxxxx   xxx
???????????????????x   xx x x
???????????????????xx xxxx xx
"""

ver, arr = to_arr(raw)

print "version", ver
print dump_arr(arr, {0:'.',1:'#',2:'~'}, True)

arr = mask(ver, arr, 0)
print dump_arr(arr, {0:'.',1:'#',2:'~'}, True)

words = walk(ver, arr)
for i, w in enumerate(words):
    print i, w

