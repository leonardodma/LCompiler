from abc import ABC, abstractmethod


class Node(ABC):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    @abstractmethod
    def evaluate(self):
        pass


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
