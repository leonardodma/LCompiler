from fileinput import filename
import sys
from parser import *


def main(argv, arc):
    filename = argv[1]
    with open(filename, "r") as file:
        source = file.read()
        print(Parser.run(source).evaluate())


if __name__ == '__main__':
    main(sys.argv, len(sys.argv))
