from abc import ABC, abstractmethod
from symbol_table import SymbolTable


class Node(ABC):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    @abstractmethod
    def evaluate(self):
        pass


class Block(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        for child in self.children:
            child.evaluate()


class Assignment(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        SymbolTable.set(self.children[0].value, self.children[1].evaluate())


class VarDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        for child in self.children:
            SymbolTable.create(child, self.value)


class Print(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        print(self.value.evaluate()[0])


class If(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        if len(self.children) == 3:
            if self.children[0].evaluate()[0]:
                self.children[1].evaluate()
            else:
                self.children[2].evaluate()
        else:
            if self.children[0].evaluate()[0]:
                self.children[1].evaluate()


class While(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        while self.children[0].evaluate()[0]:
            self.children[1].evaluate()


class Read(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        return (int(input()), "i32")


class Identifier(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        return SymbolTable.get(self.value)


class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        if self.value != ".":
            left = self.children[0].evaluate()
            right = self.children[1].evaluate()

            if left[1] == "i32" and right[1] == "i32":
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
                raise ValueError("Cannot perform operation on non-integer values")
        else:
            string_concat = ""
            for child in self.children:
                string_concat += str(child.evaluate()[0])

            return (string_concat, "String")


class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        child = self.children[0].evaluate()
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

    def evaluate(self):
        return (self.value, "i32")


class StringVal(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        return (self.value, "String")


class NoOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        pass
