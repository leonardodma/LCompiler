from tokenizer import *
from node import *


class Parser():
    tokenizer = None
    expression = ["PLUS", "MINUS"]
    term = ["MULT", "DIV"]
    factor = ["OPEN", "CLOSE"]

    @ staticmethod
    def parseExpression():
        total = Parser.parseTerm()

        while Parser.tokenizer.next.type in Parser.expression:
            op_type = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            value = Parser.parseTerm()
            total = BinOp(op_type, [total, value])

        return total

    @ staticmethod
    def parseTerm():
        total = Parser.parseFactor()

        while Parser.tokenizer.next.type in Parser.term:
            op_type = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            value = Parser.parseFactor()
            total = BinOp(op_type, [total, value])

        return total

    @ staticmethod
    def parseFactor():
        if Parser.tokenizer.next.type == "INT":
            value = IntVal(Parser.tokenizer.next.value, [])
            Parser.tokenizer.selectNext()
            return value
        elif Parser.tokenizer.next.type in Parser.expression:
            op = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            return UnOp(op, [Parser.parseFactor()])
        elif Parser.tokenizer.next.type == "OPEN":
            Parser.tokenizer.selectNext()
            value = Parser.parseExpression()
            if Parser.tokenizer.next.type != "CLOSE":
                raise ValueError("Invalid sintax: missing ')'")
            Parser.tokenizer.selectNext()
            return value
        else:
            raise ValueError(
                f"Invalid sintax: invalid token '{Parser.tokenizer.next.value}'")

    @ staticmethod
    def run(code):
        Parser.tokenizer = Tokenizer(code)
        value = Parser.parseExpression()

        if Parser.tokenizer.next.type != "EOP":
            raise ValueError("Invalid sintax")

        return value
