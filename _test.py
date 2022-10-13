from tokenizer import Tokenizer

a = Tokenizer("""
{
    x = 1;
    if ((x==2) || (x<2)) {
        Print(1);
    }
}
""")

while a.next.type != "EOP":
    print(a.next.type, "-", a.next.value)
    a.selectNext()
