programa prueba;

mini int fibonacci(int n) {
    petite int a, b, c, contador
    a = 0
    b = 1
    contador = 2
    if (n == 0 || n == 1) {
        return n
    } else {
        while (contador < n + 1 ) {
            c = a + b
            a = b
            b = c
            contador = contador + 1
        }
        return b
    }
}
main(){
    print(fibonacci(2 * 3 + 3))
}