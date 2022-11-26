from abc import ABC, abstractmethod
from tables import SymbolTable, FuncTable

int_operations = ["+", "-", "*", "/", "||", "&&"]


class Node(ABC):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, symbol_table):
        pass


class Block(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        for child in self.children:
            if child.__class__.__name__ == "Return":
                return child.evaluate(symbol_table)

            child.evaluate(symbol_table)


class Assignment(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        symbol_table.set(
            self.children[0].children[0], self.children[1].evaluate(symbol_table)
        )


class VarDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        for child in self.children:
            symbol_table.create(child, self.value)


class Print(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        print(self.value.evaluate(symbol_table)[0])


class If(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        if len(self.children) == 3:
            if self.children[0].evaluate(symbol_table)[0]:
                self.children[1].evaluate(symbol_table)
            else:
                self.children[2].evaluate(symbol_table)
        else:
            if self.children[0].evaluate(symbol_table)[0]:
                self.children[1].evaluate(symbol_table)


class While(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        while self.children[0].evaluate(symbol_table)[0]:
            self.children[1].evaluate(symbol_table)


class Read(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        return (int(input()), "i32")


class Identifier(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        if self.value == "variable":
            return symbol_table.get(self.children[0])

        return FuncTable.get(self.children[0])


class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        if self.value != ".":
            left = self.children[0].evaluate(symbol_table)
            right = self.children[1].evaluate(symbol_table)

            if self.value in int_operations and (left[1] != "i32" or right[1] != "i32"):
                raise ValueError(
                    f"Cannot perform {self.value} between {left[0]} and {right[0]}"
                )

            if self.value == "+":
                value = left[0] + right[0]
            elif self.value == "-":
                value = left[0] - right[0]
            elif self.value == "*":
                value = left[0] * right[0]
            elif self.value == "/":
                value = left[0] // right[0]
            elif self.value == "==":
                value = left[0] == right[0]
            elif self.value == "&&":
                value = left[0] and right[0]
            elif self.value == "||":
                value = left[0] or right[0]
            elif self.value == ">":
                value = left[0] > right[0]
            elif self.value == "<":
                value = left[0] < right[0]

            return (int(value), "i32")

        else:
            string_concat = ""
            for child in self.children:
                string_concat += str(child.evaluate(symbol_table)[0])

            return (string_concat, "String")


class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        child = self.children[0].evaluate(symbol_table)
        if child[1] == "i32":
            if self.value == "+":
                return (child[0], child[1])
            elif self.value == "-":
                return (-child[0], child[1])
            elif self.value == "!":
                return (not child[0], child[1])
        else:
            raise ValueError("Cannot perform operation on non-integer values")


class IntVal(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        return (self.value, "i32")


class StringVal(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        return (self.value, "String")


class FuncDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        function_type = self.value
        function_identifier = self.children[0].children[0]
        pointer = self
        FuncTable.create(function_identifier, pointer, function_type)


class FuncCall(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        arguments = []
        new_function, return_type = FuncTable.get(self.value)
        new_symbol_table = SymbolTable()

        # Apend arguments to args list
        for i in range(1, len(new_function.children) - 1):
            arguments.append(new_function.children[i].children[0])
            new_function.children[i].evaluate(new_symbol_table)

        if len(arguments) != len(self.children):
            raise ValueError("Invalid number of arguments")

        # add arguments to symbol table
        for i in range(len(arguments)):
            # check if type is correct
            new_symbol_table.set(arguments[i], self.children[i].evaluate(symbol_table))

        ret = new_function.children[-1].evaluate(new_symbol_table)

        if return_type not in ["MAIN", "VOID"]:
            if return_type != ret[1]:
                raise ValueError(
                    f"Cannot return {ret[1]} from function expecting {return_type}"
                )

        return ret


class Return(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        return self.children[0].evaluate(symbol_table)


class NoOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        pass
