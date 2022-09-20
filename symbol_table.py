class SymbolTable():
    table = {}

    @staticmethod
    def set(key, value):
        SymbolTable.table[key] = value

    @staticmethod
    def get(key):
        return SymbolTable.table[key]
