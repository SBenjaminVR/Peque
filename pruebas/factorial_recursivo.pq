programa prueba;

mini int factorial(int i) {
    if (i == 0 || i == 1) {
            return 1
    }
    else {
        return i * factorial(i - 1)
    }
}

main(){
    print(factorial(2 * 2 + 1))
}