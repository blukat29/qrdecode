import os
import subprocess

def detect(filename):
    curr = os.path.dirname(os.path.abspath(__file__))
    classpath = ".:%s/zxing.jar:%s" % (curr, curr)
    output = subprocess.check_output(["java", "-classpath", classpath, "SimpleQRDetector", filename])
    return output

