class AsmWriter:
    def __init__(self, filename):
        self.filename = filename
        self.asm = open(filename, "w")
        self.code = ""

    def write(self):
        self.asm.write(self.code)

    def close(self):
        self.asm.close()

    def add(self, text):
        self.code += text
