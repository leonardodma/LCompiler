import sys
from parser import *


def main(argv, arc):
    """
    $ nasm -f elf32 -F dwarf -g program.asm
    $ ld -m elf_i386 -o program program.o
    """
    filename = argv[1]
    # filename = "code/while.carbon"
    with open(filename, "r") as file:
        source = file.read()
        Parser.run(source, filename)


if __name__ == "__main__":
    main(sys.argv, len(sys.argv))
