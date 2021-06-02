programa prueba;

mini int fibonacci(int n) {
    petite int a 
    petite int b
    if (n == 0 || n == 1) {
        return n
    } else {
        a = fibonacci(n - 1)
        b = fibonacci(n - 2)
        return a + b
    }
}
main(){
    print(fibonacci(2 * 3 + 3))
}