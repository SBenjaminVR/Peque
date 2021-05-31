programa prueba;

mini int factorialR(int i) {
    if (i == 0 || i == 1) {
            return 1
    }
    else {
        return i * factorialR(i - 1)
    }
}

main(){
    print(factorialR(5))
}