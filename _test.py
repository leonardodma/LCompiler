from tokenizer import Tokenizer

a = Tokenizer("""
{
// Code
x_1 = 3;
y_2_ = 4;
Print(x1+y_2_+1);
}
""")

while a.next.type != "EOP":
    print(a.next.type, "-", a.next.value)
    a.selectNext()
