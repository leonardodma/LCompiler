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
