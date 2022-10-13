from tokenizer import *
from node import *


class Parser():
    tokenizer = None
    statment_semicolon = ["PRINT", "IDENTIFIER"]
    statment_brackets = ["IF", "WHILE"]

    relationExpression = ["EQUAL", "GREATER", "LESS"]
    expression = ["PLUS", "MINUS", "OR"]
    term = ["MULT", "DIV", "AND"]
    factor = ["PLUS", "MINUS", "NOT"]

    @ staticmethod
    def parseBlock():
        if Parser.tokenizer.next.type != "OPEN_BRACKTS":
            raise ValueError("Invalid sintax: block must start with '{'")

        Parser.tokenizer.selectNext()

        nodes = []
        while Parser.tokenizer.next.type != "CLOSE_BRACKTS":
            if Parser.tokenizer.next.type == "EOP":
                raise ValueError("Invalid sintax: block must end with '}'")
            node = Parser.parseStatement()
            nodes.append(node)

        Parser.tokenizer.selectNext()

        return Block("block", nodes)

    @ staticmethod
    def parseStatement():
        if Parser.tokenizer.next.type == "SEMICOLON":
            Parser.tokenizer.selectNext()
            return NoOp("", [])
        elif Parser.tokenizer.next.type in Parser.statment_semicolon:
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

        elif Parser.tokenizer.next.type in Parser.statment_brackets:
            if Parser.tokenizer.next.type == "IF":
                Parser.tokenizer.selectNext()

                if Parser.tokenizer.next.type != "OPEN_PARENTHESES":
                    raise ValueError("Invalid sintax: if must have '('")

                Parser.tokenizer.selectNext()
                condition = Parser.parseRelationExpression()

                if Parser.tokenizer.next.type != "CLOSE_PARENTHESES":
                    raise ValueError("Invalid sintax: if must have ')'")

                Parser.tokenizer.selectNext()
                if_statement = Parser.parseStatement()

                if Parser.tokenizer.next.type == "ELSE":
                    Parser.tokenizer.selectNext()
                    else_statement = Parser.parseStatement()
                    return If("IF", [condition, if_statement, else_statement])

                return If("IF", [condition, if_statement])

            elif Parser.tokenizer.next.type == "WHILE":
                Parser.tokenizer.selectNext()

                if Parser.tokenizer.next.type != "OPEN_PARENTHESES":
                    raise ValueError("Invalid sintax: while must have '('")

                Parser.tokenizer.selectNext()
                condition = Parser.parseRelationExpression()

                if Parser.tokenizer.next.type != "CLOSE_PARENTHESES":
                    raise ValueError("Invalid sintax: while must have ')'")

                Parser.tokenizer.selectNext()

                return While("WHILE", [condition, Parser.parseStatement()])

        elif Parser.tokenizer.next.type == "INT":
            raise ValueError("Invalid sintax: int must not be assigned")

        else:
            return Parser.parseBlock()

    @ staticmethod
    def parseRelationExpression():
        result = Parser.parseExpression()

        while Parser.tokenizer.next.type in Parser.relationExpression:
            op_type = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            value = Parser.parseExpression()
            result = BinOp(op_type, [result, value])

        return result

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
        elif Parser.tokenizer.next.type in Parser.factor:
            op = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            return UnOp(op, [Parser.parseFactor()])
        elif Parser.tokenizer.next.type == "OPEN_PARENTHESES":
            Parser.tokenizer.selectNext()
            value = Parser.parseRelationExpression()
            if Parser.tokenizer.next.type != "CLOSE_PARENTHESES":
                raise ValueError("Invalid sintax: missing ')'")

            Parser.tokenizer.selectNext()
            return value
        elif Parser.tokenizer.next.type == "READ":
            Parser.tokenizer.selectNext()

            if Parser.tokenizer.next.type != "OPEN_PARENTHESES":
                raise ValueError("Invalid sintax: read must have '('")

            Parser.tokenizer.selectNext()
            result = Read("READ", [])

            if Parser.tokenizer.next.type != "CLOSE_PARENTHESES":
                raise ValueError("Invalid sintax: read must have ')'")
            Parser.tokenizer.selectNext()

            return result
        else:
            raise ValueError(
                f"Invalid sintax: invalid token '{Parser.tokenizer.next.value}'")

    @ staticmethod
    def run(code):
        Parser.tokenizer = Tokenizer(code)
        blocks = Parser.parseBlock()
        if Parser.tokenizer.next.type != "EOP":
            raise ValueError("Invalid sintax: block must end with '}'")

        blocks.evaluate()
