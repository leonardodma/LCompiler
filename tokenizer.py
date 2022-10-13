import re


class Token:
    def __init__(self, type: str, value):
        self.type = type
        self.value = value


class PrePro:
    @staticmethod
    def filter(source: str):
        source = re.sub(re.compile("//.*?\n"), "", source)
        source = re.sub("\s+", " ", source)
        return source.replace("\n", "")


class Tokenizer:
    def __init__(self, source: str):
        self.source = PrePro.filter(source)
        self.position = 0

        self.operations = {
            "+": "PLUS",
            "-": "MINUS",
            "*": "MULT",
            "/": "DIV",
            "(": "OPEN_PARENTHESES",
            ")": "CLOSE_PARENTHESES",
            "{": "OPEN_BRACKTS",
            "}": "CLOSE_BRACKTS",
            "=": "ASSIGNMENT",
            "==": "EQUAL",
            ";": "SEMICOLON",
            "!": "NOT",
            ">": "GREATER",
            "<": "LESS",
            "|": "OR",
            "||": "OR",
            "&&": "AND",
            "&": "AND",
        }

        self.selectNext()

    def selectNext(self):
        source = self.source[self.position:]

        if self.position >= len(self.source) or source.replace(" ", "") == "":
            self.next = Token("EOP", None)
        else:
            space = False
            value = ""
            i = 0
            for token in source:
                if token == " ":
                    space = True
                    self.position += 1

                elif token.isdigit() or token.isalpha() or token == "_":
                    if value.isdigit() and not token.isdigit():
                        raise ValueError(
                            "Invalid sintax: variables must not start with a number"
                        )

                    value += token
                    self.position += 1

                    if space and self.next.value not in self.operations.keys():
                        print("valor", self.next.value)
                        raise ValueError(
                            f"Invalid sintax: no operator between values")
                    elif i + 1 >= len(source):
                        if value.isdigit():
                            self.next = Token("INT", int(value))
                        elif value.isalpha():
                            self.next = Token("IDENTIFIER", value)
                        break

                elif value != "" and (token in self.operations.keys() or token == " "):
                    try:
                        value = int(value)
                        self.next = Token("INT", value)
                    except ValueError:
                        if value == "Print":
                            self.next = Token("PRINT", value)
                        elif value == "Read":
                            self.next = Token("READ", value)
                        elif value == "if":
                            self.next = Token("IF", value)
                        elif value == "else":
                            self.next = Token("ELSE", value)
                        elif value == "while":
                            self.next = Token("WHILE", value)
                        else:
                            self.next = Token("IDENTIFIER", value)
                    break

                elif value == "" and token in self.operations.keys():
                    if token == "=" and source[i + 1] == "=":
                        self.next = Token("EQUAL", "==")
                        self.position += 2
                    elif token == "&" and source[i + 1] == "&":
                        self.next = Token(self.operations["&"], "&&")
                        self.position += 2
                    elif token == "|" and source[i + 1] == "|":
                        self.next = Token(self.operations["|"], "||")
                        self.position += 2
                    else:
                        self.next = Token(self.operations[token], token)
                        self.position += 1

                    break
                else:
                    raise ValueError(
                        f"Invalid sintax: invalid token '{token}'")

                i += 1
