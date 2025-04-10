import os
import sys
import subprocess
import re

def main():
    py_dir = os.path.dirname(os.path.abspath(__file__))
    txt_req = os.path.join(py_dir, "preconditions.txt")

    f = open(txt_req, "r")

    g = subprocess.check_output("pip list")
    g = g.decode("utf-8")

    installed = re.findall(r'(?<=\r\n)\w+', g)

    for line in f:
        needed = line.replace("\n", "")
        if needed in installed:
            print("Module " + needed + " is already installed")
        else:
            os.system("pip install " + needed)

if __name__ == "__main__":
    main()