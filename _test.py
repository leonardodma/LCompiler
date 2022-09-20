from tokenizer import Tokenizer

a = Tokenizer("""
{
Print(40+-+-2);
Print(40+--2);
}
""")

while a.next.type != "EOP":
    print(a.next.type, "-", a.next.value)
    a.selectNext()
