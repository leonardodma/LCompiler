from tokenizer import Tokenizer

a = Tokenizer("""
{
    a = 1;
    while (a  == 1)
    {
        Print(a);
    }
}
""")

while a.next.type != "EOP":
    print(a.next.type, "-", a.next.value)
    a.selectNext()
