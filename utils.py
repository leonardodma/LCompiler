class Token():
    def __init__(self, type: str, value):
        self.type = type
        self.value = value


class Tokenizer():
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.operations = {"+": "PLUS", "-": "MINUS"}

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
                self.next = Token("INT", int(value))
                break
            elif token.isdigit():
                value += token
            else:
                raise ValueError(f"Invalid sintax: invalid token '{token}'")

        self.position += 1

    def selectNext(self):
        if self.position >= len(self.source):
            if self.next.value in self.operations.keys():
                raise ValueError(
                    "Invalid sintax: string must not end with an operation")
            self.next = Token("EOP", None)
        else:
            source = self.source[self.position:]
            print("Source:" + source)
            space = False
            value = ""
            i = 0
            for token in source:
                print("Value: " + value)
                print("Token: " + token)
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
                    print("Entrou")
                    print(token)

                i += 1


class Parser():
    tokenizer = None

    @ staticmethod
    def parseExpression():
        total = Parser.tokenizer.next.value

        while Parser.tokenizer.next.type != "EOP":
            Parser.tokenizer.selectNext()
            print(Parser.tokenizer.next.value)
            print(Parser.tokenizer.next.type)
            print("----------")

            if Parser.tokenizer.next.type == "PLUS":
                Parser.tokenizer.selectNext()
                total += Parser.tokenizer.next.value
            elif Parser.tokenizer.next.type == "MINUS":
                Parser.tokenizer.selectNext()
                total -= Parser.tokenizer.next.value

        return total

    @ staticmethod
    def run(code):
        Parser.tokenizer = Tokenizer(code)

        return Parser.parseExpression()
