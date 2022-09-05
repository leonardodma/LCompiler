from signal import signal


class Token():
    def __init__(self, type: str, value):
        self.type = type
        self.value = value


class PrePro():
    @staticmethod
    def filter(source: str):
        return source.split("//")[0]


class Tokenizer():
    def __init__(self, source: str):
        self.source = PrePro.filter(source)
        self.position = 0
        self.operations = {"+": "PLUS", "-": "MINUS",
                           "*": "MULT", "/": "DIV",
                           "(": "OPEN", ')': "CLOSE"}

        self.selectNext()

    def selectNext(self):
        source = self.source[self.position:]

        if self.position >= len(self.source) or source.replace(" ", "") == "":
            if self.next.value in self.operations.keys() and self.next.value != ")":
                raise ValueError(
                    "Invalid sintax: string must not end with an operation")
            self.next = Token("EOP", None)
        else:
            space = False
            value = ""
            i = 0
            for token in source:
                if token == " ":
                    space = True
                    self.position += 1
                    if i + 1 >= len(source) and value.isdigit():
                        self.next = Token("INT", int(value))
                        break

                elif token.isdigit():
                    value += token
                    self.position += 1

                    if space and self.next.value not in self.operations.keys():
                        raise ValueError(
                            f"Invalid sintax: no operations between numbers")
                    elif i + 1 >= len(source):
                        self.next = Token("INT", int(value))
                        break

                elif value != "" and (token in self.operations.keys() or token == " "):
                    self.next = Token("INT", int(value))
                    break

                elif value == "" and token in self.operations.keys():
                    self.next = Token(self.operations[token], token)
                    self.position += 1
                    break
                else:
                    raise ValueError(
                        f"Invalid sintax: invalid token '{token}'")

                i += 1


class Parser():
    tokenizer = None
    expression = ["PLUS", "MINUS"]
    term = ["MULT", "DIV"]
    factor = ["OPEN", "CLOSE"]

    @ staticmethod
    def parseExpression():
        total = Parser.parseTerm()

        while Parser.tokenizer.next.type in Parser.expression:
            op_type = Parser.tokenizer.next.type
            Parser.tokenizer.selectNext()
            value = Parser.parseTerm()

            if op_type == "PLUS":
                total += value
            elif op_type == "MINUS":
                total -= value

        return total

    @ staticmethod
    def parseTerm():
        total = Parser.parseFactor()

        while Parser.tokenizer.next.type in Parser.term:
            op_type = Parser.tokenizer.next.type
            Parser.tokenizer.selectNext()
            value = Parser.parseFactor()

            if op_type == "MULT":
                total *= value
            elif op_type == "DIV":
                total //= value

        return total

    @ staticmethod
    def parseFactor():
        if Parser.tokenizer.next.type == "INT":
            value = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            return value
        elif Parser.tokenizer.next.type in Parser.expression:
            if Parser.tokenizer.next.type == "PLUS":
                Parser.tokenizer.selectNext()
                return Parser.parseFactor()
            elif Parser.tokenizer.next.type == "MINUS":
                Parser.tokenizer.selectNext()
                return -Parser.parseFactor()
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
