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

        self.reserved_words = {
            "if": "IF",
            "else": "ELSE",
            "while": "WHILE",
            "Print": "PRINT",
            "Read": "READ",
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
                if token == " " or token in self.operations.keys():
                    if value != "":
                        try:
                            value = int(value)
                            self.next = Token("INT", value)
                        except:
                            if value in self.reserved_words.keys():
                                self.next = Token(self.reserved_words[value], value)
                            else:
                                self.next = Token("IDENTIFIER", value)
                        break

                    elif value == "" and token != " ":
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
                        space = True
                        self.position += 1

                elif token.isdigit() or token.isalpha() or token == "_":
                    if value.isdigit() and not token.isdigit():
                        raise ValueError(
                            "Invalid sintax: variables must not start with a number"
                        )

                    value += token
                    self.position += 1

                else:
                    raise ValueError(
                        f"Invalid sintax: invalid token '{token}'")

                i += 1
