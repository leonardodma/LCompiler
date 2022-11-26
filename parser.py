from tokenizer import *
from node import *


class Parser:
    tokenizer = None
    statment_semicolon = ["PRINT", "IDENTIFIER", "VAR", "RETURN"]
    statment_brackets = ["IF", "WHILE"]

    relationExpression = ["EQUAL", "GREATER", "LESS", "DOT"]
    expression = ["PLUS", "MINUS", "OR"]
    term = ["MULT", "DIV", "AND"]
    factor = ["PLUS", "MINUS", "NOT"]

    @staticmethod
    def parseProgram():
        nodes = []
        while Parser.tokenizer.next.type != "EOP":
            node = Parser.parseDeclaration()
            nodes.append(node)

        Parser.tokenizer.selectNext()

        # Add main function func call
        nodes.append(FuncCall("Main", []))

        return Block("Program", nodes)

    @staticmethod
    def parseDeclaration():
        if Parser.tokenizer.next.type == "FUNCTION":
            Parser.tokenizer.selectNext()
            function_identifier = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()

            if Parser.tokenizer.next.type != "OPEN_PARENTHESES":
                raise ValueError("Expected '(' after function identifier")
            Parser.tokenizer.selectNext()

            arguments: list[FuncDec] = []
            var_identifiers: list[str] = []
            while Parser.tokenizer.next.type != "CLOSE_PARENTHESES":
                if var_identifiers == []:
                    if Parser.tokenizer.next.type != "IDENTIFIER":
                        raise ValueError("Expected identifier after '('")

                    var_identifier = Parser.tokenizer.next.value
                    var_identifiers = [var_identifier]
                    Parser.tokenizer.selectNext()

                if Parser.tokenizer.next.type == "COMMA":
                    while Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.selectNext()
                        if Parser.tokenizer.next.type != "IDENTIFIER":
                            raise ValueError("Expected identifier after ','")

                        var_identifiers.append(Parser.tokenizer.next.value)
                        Parser.tokenizer.selectNext()

                elif Parser.tokenizer.next.type == "COLON":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type not in ["STRING_TYPE", "INT_TYPE"]:
                        raise ValueError("Expected variable type after ':'")

                    var_type = Parser.tokenizer.next.value
                    Parser.tokenizer.selectNext()

                    if Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.selectNext()

                    arguments.append(VarDec(var_type, var_identifiers))
                    var_identifiers = []

            # var declarations made, stored in arguments
            Parser.tokenizer.selectNext()
            function_type = "VOID" if function_identifier != "Main" else "MAIN"
            if Parser.tokenizer.next.type == "ARROW":
                # get return type
                Parser.tokenizer.selectNext()
                function_type = Parser.tokenizer.next.value
                if function_type not in ["i32", "String"]:
                    raise ValueError("Expected variable type i32 or String after '->'")
                Parser.tokenizer.selectNext()

            # Create children of funcdec
            children = [Identifier("function", [function_identifier])]

            # Add arguments to children
            for argument in arguments:
                children.append(argument)

            # add the block node
            children.append(Parser.parseBlock())

            return FuncDec(function_type, children)

        else:
            raise ValueError("Invalid declaration of function")

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
                var_identifiers = []
                var_declaration = True
                while var_declaration:
                    if Parser.tokenizer.next.type != "IDENTIFIER":
                        raise ValueError(
                            "Invalid sintax: variable declaration must start with identifier"
                        )

                    var_identifiers.append(Parser.tokenizer.next.value)
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

                value = VarDec(var_type, var_identifiers)

            elif Parser.tokenizer.next.type == "IDENTIFIER":
                identifier_token = Parser.tokenizer.next.value
                identifier = Identifier("variable", [identifier_token])
                Parser.tokenizer.selectNext()

                # Var assignment
                if Parser.tokenizer.next.type == "ASSIGNMENT":
                    Parser.tokenizer.selectNext()
                    value = Assignment(
                        "Assigment", [identifier, Parser.parseRelationExpression()]
                    )
                # Function call
                elif Parser.tokenizer.next.type == "OPEN_PARENTHESES":
                    Parser.tokenizer.selectNext()
                    arguments = []
                    while Parser.tokenizer.next.type != "CLOSE_PARENTHESES":
                        arguments.append(Parser.parseRelationExpression())
                        if Parser.tokenizer.next.type == "COMMA":
                            Parser.tokenizer.selectNext()

                    Parser.tokenizer.selectNext()
                    value = FuncCall(identifier_token, arguments)

            elif Parser.tokenizer.next.type == "PRINT":
                Parser.tokenizer.selectNext()

                if Parser.tokenizer.next.type != "OPEN_PARENTHESES":
                    raise ValueError("Invalid sintax: print must have '('")

                Parser.tokenizer.selectNext()
                value = Print(Parser.parseRelationExpression(), [])

                if Parser.tokenizer.next.type != "CLOSE_PARENTHESES":
                    raise ValueError("Invalid sintax: print must have ')'")

                Parser.tokenizer.selectNext()

            elif Parser.tokenizer.next.type == "RETURN":
                Parser.tokenizer.selectNext()
                value = Return("RETURN", [Parser.parseRelationExpression()])

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
            identifier_token = Parser.tokenizer.next.value
            identifier = Identifier("variable", [identifier_token])
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "OPEN_PARENTHESES":
                Parser.tokenizer.selectNext()
                arguments = []
                while Parser.tokenizer.next.type != "CLOSE_PARENTHESES":
                    arguments.append(Parser.parseRelationExpression())
                    if Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.selectNext()

                Parser.tokenizer.selectNext()
                return FuncCall(identifier_token, arguments)

            return identifier

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
    def run(code):
        Parser.tokenizer = Tokenizer(code)
        symbol_table = SymbolTable()
        blocks = Parser.parseProgram()
        blocks.evaluate(symbol_table)
