import sys
from utils import *

def main(argv, arc):
    print(Parser.run(argv[1]))

if __name__ == '__main__':
    main(sys.argv, len(sys.argv))