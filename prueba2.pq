programa prueba;

mini int factorial(int i) {
    petite int c
    petite int fact
    fact = 1
    if (i < 0) {
        c = 0
    }
    else {
        if (i == 0 || i == 1) {
            c = 1
        }
        else {
            while (i > 1) {
                fact = fact * i
                i = i - 1
            }
        }
    }
    if (fact <> 1) {
        c = fact
    }
    print(fact)
    return c
}

mini int factorialR(int i) {
    petite int c 
    if (i == 0 || i == 1) {
            c = 1
    }
    else {
        c = i * factorialR(i - 1)
    }
    return c
}

main(){
    print(factorialR(5))
}