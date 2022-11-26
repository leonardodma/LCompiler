class SymbolTable:
    """
    Store in the symbol table: (var_identifier, var_type)
    """

    def __init__(self):
        self.table = {}

    def set(self, key, value):
        if key not in self.table.keys():
            raise ValueError(f"Variable {key} type was not declared to be assigned")

        var_identifier, var_type = self.table[key]

        if var_type != value[1]:
            raise ValueError(f"Variable {key} type is {var_type} not {value[1]}")

        var_identifier = value[0]
        self.table[key] = (var_identifier, var_type)

    def get(self, key):
        if key not in self.table.keys():
            raise ValueError(f"Variable {key} was not declared")
        return self.table[key]

    def create(self, var_identifier, var_type):
        if var_identifier in self.table.keys():
            raise ValueError(f"Variable {var_identifier} already declared")

        if var_type == "i32":
            self.table[var_identifier] = (0, var_type)
        elif var_type == "String":
            self.table[var_identifier] = ("", var_type)


class FuncTable:
    """
    Store in FuncTable: (pointer, return_type)
    """

    table = {}

    def get(key):
        if key not in FuncTable.table.keys():
            raise ValueError(f"Function {key} not declared")
        return FuncTable.table[key]

    def create(key, pointer, return_type):
        if key in FuncTable.table.keys():
            raise ValueError(f"Function {key} already declared")
        FuncTable.table[key] = (pointer, return_type)
