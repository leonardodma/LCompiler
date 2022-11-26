fn soma(a: i32, y: i32) -> i32 {
    return a + y;
}

fn subtracao(a: i32, y: i32) -> i32 {
    return a - y;
}

fn concat(a: String, y: String) -> String {
    return a . y;
}

fn print(a: String) {
    Print(a);
}

fn Main() {
    var a: i32;
    var b: i32;
    var c: i32;
    a = 3;
    b = soma(a, 4);
    c = subtracao(a, 4);
    print("Hello World", "!");

    Print(b);
    Print(c);
}