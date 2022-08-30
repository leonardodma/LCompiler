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
        self.operations = {"+": "PLUS", "-": "MINUS", "*": "MULT", "/": "DIV"}

        self.fistToken()

    def fistToken(self):
        value = ""
        for token in self.source:
            if value == "" and (token in self.operations.keys() or token == " "):
                raise ValueError(
                    "Invalid sintax: your input should not start with an operation or empty string.")
            elif value != "" and (token in self.operations.keys() or token == " "):
                self.next = Token("INT", int(value))
                break
            elif self.position + 1 >= len(self.source):
                value += token
                self.position += 1
                self.next = Token("INT", int(value))
                break
            elif token.isdigit():
                value += token
            else:
                raise ValueError(f"Invalid sintax: invalid token '{token}'")

            self.position += 1

    def selectNext(self):
        source = self.source[self.position:]
        if self.position >= len(self.source) or source.replace(" ", "") == "":
            if self.next.value in self.operations.keys():
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
                    if self.next.type != "INT":
                        raise ValueError(
                            f"Invalid Sintax: two operators in a row")
                    self.next = Token(self.operations[token], token)
                    self.position += 1
                    break
                else:
                    raise ValueError(
                        f"Invalid sintax: invalid token '{token}'")

                i += 1


class Parser():
    tokenizer = None
    term = ["MULT", "DIV"]
    expression = ["PLUS", "MINUS"]

    @ staticmethod
    def parseExpression():
        total = 0
        while Parser.tokenizer.next.type != "EOP":
            op_type = Parser.tokenizer.next.type
            value = Parser.parseTerm()

            if op_type == "MINUS":
                total -= value
            else:
                if op_type != "EOP":
                    total += value

            # Parser.tokenizer.selectNext()

        return total

    @ staticmethod
    def parseTerm():
        if Parser.tokenizer.next.type != "INT":
            Parser.tokenizer.selectNext()

        total = Parser.tokenizer.next.value
        Parser.tokenizer.selectNext()
        op_type = Parser.tokenizer.next.type

        while op_type in Parser.term:
            if op_type == "MULT":
                Parser.tokenizer.selectNext()
                total *= Parser.tokenizer.next.value
            elif op_type == "DIV":
                Parser.tokenizer.selectNext()
                total //= Parser.tokenizer.next.value

            Parser.tokenizer.selectNext()
            op_type = Parser.tokenizer.next.type

        return total

    @ staticmethod
    def run(code):
        Parser.tokenizer = Tokenizer(code)

        return Parser.parseExpression()
