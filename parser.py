from tokenizer import *
from node import *
from assembler import CodeAssembler
from asm_writer import AsmWriter


class Parser:
    tokenizer = None
    statment_semicolon = ["PRINT", "IDENTIFIER", "VAR"]
    statment_brackets = ["IF", "WHILE"]

    relationExpression = ["EQUAL", "GREATER", "LESS", "DOT"]
    expression = ["PLUS", "MINUS", "OR"]
    term = ["MULT", "DIV", "AND"]
    factor = ["PLUS", "MINUS", "NOT"]

    @staticmethod
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

        return Block("BLOCK", nodes)

    @staticmethod
    def parseStatement():
        if Parser.tokenizer.next.type == "SEMICOLON":
            Parser.tokenizer.selectNext()
            return NoOp("NOP", [])
        elif Parser.tokenizer.next.type in Parser.statment_semicolon:
            if Parser.tokenizer.next.type == "VAR":
                Parser.tokenizer.selectNext()
                variables = []
                var_declaration = True
                while var_declaration:
                    if Parser.tokenizer.next.type != "IDENTIFIER":
                        raise ValueError(
                            "Invalid sintax: variable declaration must start with identifier"
                        )

                    variables.append(Parser.tokenizer.next.value)
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type != "COMMA":
                        var_declaration = False
                    else:
                        Parser.tokenizer.selectNext()

                # Check the : token to set variable type
                if Parser.tokenizer.next.type != "COLON":
                    raise ValueError(
                        "Invalid sintax: variable declaration must have ':' before setting type"
                    )

                Parser.tokenizer.selectNext()
                var_type = Parser.tokenizer.next.value

                if var_type not in ["i32", "String"]:
                    raise ValueError(
                        f"Invalid sintax: variable type must be 'i32' or 'String', not {var_type}"
                    )
                Parser.tokenizer.selectNext()

                value = VarDec(var_type, variables)

            elif Parser.tokenizer.next.type == "IDENTIFIER":
                identifier_token = Parser.tokenizer.next.value
                identifier = Identifier(identifier_token, [])

                Parser.tokenizer.selectNext()

                if Parser.tokenizer.next.type != "ASSIGNMENT":
                    raise ValueError(
                        f"Invalid sintax: assignment of '{identifier_token}' did not use '='"
                    )

                Parser.tokenizer.selectNext()

                value = Assignment(
                    "Assigment", [identifier, Parser.parseRelationExpression()]
                )

            elif Parser.tokenizer.next.type == "PRINT":
                Parser.tokenizer.selectNext()

                if Parser.tokenizer.next.type != "OPEN_PARENTHESES":
                    raise ValueError("Invalid sintax: print must have '('")

                Parser.tokenizer.selectNext()
                value = Print(Parser.parseRelationExpression(), [])

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

    @staticmethod
    def parseRelationExpression():
        result = Parser.parseExpression()

        while Parser.tokenizer.next.type in Parser.relationExpression:
            op_type = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            value = Parser.parseExpression()
            result = BinOp(op_type, [result, value])

        return result

    @staticmethod
    def parseExpression():
        total = Parser.parseTerm()

        while Parser.tokenizer.next.type in Parser.expression:
            op_type = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            value = Parser.parseTerm()
            total = BinOp(op_type, [total, value])

        return total

    @staticmethod
    def parseTerm():
        total = Parser.parseFactor()

        while Parser.tokenizer.next.type in Parser.term:
            op_type = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            value = Parser.parseFactor()
            total = BinOp(op_type, [total, value])

        return total

    @staticmethod
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

        elif Parser.tokenizer.next.type == "STRING":
            value = StringVal(Parser.tokenizer.next.value, [])
            Parser.tokenizer.selectNext()
            return value

        else:
            raise ValueError(
                f"Invalid sintax: invalid token '{Parser.tokenizer.next.value}'"
            )

    @staticmethod
    def run(code, filename):
        Parser.tokenizer = Tokenizer(code)

        # Write code initial template
        writer = AsmWriter(filename.split(".")[0] + ".asm")
        writer.add(CodeAssembler.initialize())

        # Get the blocks
        blocks = Parser.parseBlock()
        if Parser.tokenizer.next.type != "EOP":
            raise ValueError("Invalid sintax: block must end with '}'")

        # Add the blocks to the code
        writer.add(blocks.evaluate())

        # Write the code end template
        writer.add(CodeAssembler.end())
        writer.write()
        writer.close()
