from tokenizer import Tokenizer

a = Tokenizer(
    """
{
    var a : i32;
    var b : String;
    a = 1;
    b = "Hello";

    if (a < 10)
    {
        Print("entrou");
    }

    
    Print("saiu");
}
"""
)

while a.next.type != "EOP":
    print(a.next.type, "-", a.next.value)
    a.selectNext()
