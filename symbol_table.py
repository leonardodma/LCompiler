class SymbolTable:
    table = {}

    @staticmethod
    def set(key, value):
        if key[0] not in SymbolTable.table.keys():
            raise ValueError(f"Variable {key[0]} type was not declared to be assigned")

        var_identifier, var_type = SymbolTable.table[key]

        if var_type != value[1]:
            raise ValueError(f"Variable {key} type is {var_type} not {value[1]}")

        var_identifier = value[0]
        SymbolTable.table[key] = (var_identifier, var_type)

    @staticmethod
    def get(key):
        return SymbolTable.table[key]

    @staticmethod
    def create(var_identifier, var_type):
        if var_identifier in SymbolTable.table.keys():
            raise ValueError(f"Variable {var_identifier} already declared")

        if var_type == "i32":
            SymbolTable.table[var_identifier] = (0, var_type)
        elif var_type == "String":
            SymbolTable.table[var_identifier] = ("", var_type)
