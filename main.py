import sys
from parser import *


def main(argv, arc):
    print(Parser.run(argv[1]).evaluate())


if __name__ == '__main__':
    main(sys.argv, len(sys.argv))
