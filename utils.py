class Token():
    def __init__(self, type: str, value):
        self.type = type
        self.value = value


class Tokenizer():
    def __init__(self, source: str):
        self.source = source.replace(" ", "")
        self.position = 0
        self.operations = {"+": "PLUS", "-": "MINUS"}

        value = ""
        for char in self.source:
            if char != " ":
                if value == "" and char in self.operations.keys():
                    raise ValueError(
                        "Invalid sintax: your input should not start with an operation")
                elif value != "" and char in self.operations.keys():
                    self.next = Token("INT", int(value))
                    break
                elif self.position + 1 >= len(self.source):
                    value += char
                    self.next = Token("INT", int(value))
                    break
                elif char.isdigit():
                    value += char
                else:
                    raise ValueError(f"Invalid sintax: invalid token '{char}'")

            self.position += 1

    def selectNext(self):
        if self.position >= len(self.source):
            self.next = Token("EOP", None)
        else:
            source = self.source[self.position:]
            value = ""

            for i in range(len(source)):
                char = source[i]

                if char != " ":
                    if char.isdigit() or char in self.operations.keys():
                        if char.isdigit():
                            value += char
                            # End of operation
                            if i + 1 >= len(source):
                                self.next = Token("INT", int(value))
                                self.position += 1
                                break

                        else:
                            if value == "":
                                if self.next.type in self.operations.values():
                                    raise ValueError(
                                        "Invalid Sintax: two operators in a row")
                                elif i + 1 >= len(source):
                                    raise ValueError(
                                        "Can not end with an operator")
                                self.next = Token(self.operations[char], char)
                                self.position += 1

                            else:
                                self.next = Token("INT", int(value))

                            break
                    else:
                        raise ValueError(
                            f"Invalid sintax: invalid token '{char}'")

                self.position += 1


class Parser():
    tokenizer = None

    @ staticmethod
    def parseExpression():
        total = Parser.tokenizer.next.value
        while Parser.tokenizer.next.type != "EOP":
            Parser.tokenizer.selectNext()

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
