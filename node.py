from abc import ABC, abstractmethod
from symbol_table import SymbolTable
from assembler import CodeAssembler


int_operations = ["+", "-", "*", "/", "||", "&&"]


class Node(ABC):
    i = 0

    def __init__(self, value, children):
        self.value = value
        self.children = children

    @abstractmethod
    def evaluate(self):
        pass

    def newId():
        Node.i += 1
        return Node.i


class Block(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        block = ""
        for child in self.children:
            code = child.evaluate()
            block += "\n\t" + code

        return block


class Assignment(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        # SymbolTable.set(self.children[0].value, self.children[1].evaluate())
        pointer = SymbolTable.get(self.children[0].value)[0]
        child = self.children[1].evaluate()
        return CodeAssembler.assigment(child, pointer)


class VarDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        for child in self.children:
            SymbolTable.create(child, self.value)

        return CodeAssembler.varDec()


class Print(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        # print(self.value.evaluate()[0])
        return CodeAssembler.print(self.value.evaluate())


class If(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        self.id = Node.newId()
        if len(self.children) == 3:
            return CodeAssembler.ifElseStatement(
                self.id,
                self.children[0].evaluate(),
                self.children[1].evaluate(),
                self.children[2].evaluate(),
            )
        else:
            return CodeAssembler.ifStatement(
                self.id, self.children[0].evaluate(), self.children[1].evaluate()
            )


class While(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        """while self.children[0].evaluate()[0]:
        self.children[1].evaluate()"""

        self.id = Node.newId()
        condition = self.children[0].evaluate()
        statement = self.children[1].evaluate()

        return CodeAssembler.whileLoop(self.id, condition, statement)


class Read(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        """return (int(input()), "i32")"""


class Identifier(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        """return SymbolTable.get(self.value)"""

        pointer = SymbolTable.get(self.value)[0]
        return CodeAssembler.identifier(pointer)


class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        left = self.children[0].evaluate()
        right = self.children[1].evaluate()

        """ if self.value in int_operations and (left[1] != "i32" or right[1] != "i32"):
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
            value = left[0] < right[0] """

        return CodeAssembler.binOp(self.value, left, right)


class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        value = self.children[0].value
        child = self.children[0].evaluate()

        if type(value) != int and value not in ["+", "-", "!"]:
            pointer = SymbolTable.get(value)[0]
            return CodeAssembler.unOp(self.value, child, f"[EBP-{pointer}]")
        elif type(value) == int:
            return CodeAssembler.unOp(self.value, child, value)

        return CodeAssembler.unOp(self.value, child, "EBX")


class IntVal(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        return CodeAssembler.intVal(self.value)
        # return (self.value, "i32")


class StringVal(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        """return (self.value, "String")"""


class NoOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        pass
