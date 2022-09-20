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


class Print(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        print(self.value.evaluate())


class Identifier(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        return SymbolTable.get(self.value)


class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        if self.value == "+":
            return self.children[0].evaluate() + self.children[1].evaluate()
        elif self.value == "-":
            return self.children[0].evaluate() - self.children[1].evaluate()
        elif self.value == "*":
            return self.children[0].evaluate() * self.children[1].evaluate()
        elif self.value == "/":
            return self.children[0].evaluate() // self.children[1].evaluate()


class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        if self.value == "+":
            return self.children[0].evaluate()
        elif self.value == "-":
            return -self.children[0].evaluate()


class IntVal(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        return self.value


class NoOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        pass
