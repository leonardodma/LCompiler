from tokenizer import *
from node import *


class Parser():
    tokenizer = None
    statment = ["PRINT", "IDENTIFIER"]
    blok = ["OPEN_BRACKTS", "CLOSE_BRACKTS"]
    expression = ["PLUS", "MINUS"]
    term = ["MULT", "DIV"]
    factor = ["OPEN_PARENTHESES", "CLOSE_PARENTHESES"]

    @ staticmethod
    def parseBlock():
        if Parser.tokenizer.next.type != "OPEN_BRACKTS":
            raise ValueError("Invalid sintax: block must start with '{'")

        Parser.tokenizer.selectNext()

        nodes = []
        while Parser.tokenizer.next.type != "CLOSE_BRACKTS":
            if Parser.tokenizer.next.type == "EOP":
                raise ValueError("Invalid sintax: block must end with '}'")
            nodes.append(Parser.parseStatement())

        Parser.tokenizer.selectNext()
        if Parser.tokenizer.next.type != "EOP":
            raise ValueError("Invalid sintax: block must end with '}'")

        Block("", nodes).evaluate()

    @ staticmethod
    def parseStatement():
        if Parser.tokenizer.next.type in Parser.statment:
            if Parser.tokenizer.next.type == "IDENTIFIER":
                identifier = Identifier(Parser.tokenizer.next.value, [])
                Parser.tokenizer.selectNext()

                if Parser.tokenizer.next.type != "ASSIGNMENT":
                    raise ValueError(
                        "Invalid sintax: assignment must have '='")

                Parser.tokenizer.selectNext()

                value = Assignment(
                    "Assigment", [identifier, Parser.parseExpression()])

            elif Parser.tokenizer.next.type == "PRINT":
                Parser.tokenizer.selectNext()

                if Parser.tokenizer.next.type != "OPEN_PARENTHESES":
                    raise ValueError("Invalid sintax: print must have '('")

                Parser.tokenizer.selectNext()
                value = Print(Parser.parseExpression(), [])

                if Parser.tokenizer.next.type != "CLOSE_PARENTHESES":
                    raise ValueError("Invalid sintax: print must have ')'")

                Parser.tokenizer.selectNext()

            # Check if the statement ends with ';'
            if Parser.tokenizer.next.type != "SEMICOLON":
                raise ValueError("Invalid sintax: line didn't end with  ';'")

            Parser.tokenizer.selectNext()
            return value

        elif Parser.tokenizer.next.type == "INT":
            raise ValueError("Invalid sintax: int must not be assigned")

        else:
            if Parser.tokenizer.next.type != "SEMICOLON":
                print("Entrou")
                raise ValueError("Invalid sintax: no atribuition were made")

            Parser.tokenizer.selectNext()
            return NoOp("NoOp", [])

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
        elif Parser.tokenizer.next.type == "IDENTIFIER":
            value = Identifier(Parser.tokenizer.next.value, [])
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
        Parser.parseBlock()
