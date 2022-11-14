from tokenizer import Tokenizer

a = Tokenizer(
    """
{
    var x : i32;
    x = 1;
    Print(-x);
}
"""
)

while a.next.type != "EOP":
    print(a.next.type, "-", a.next.value)
    a.selectNext()
