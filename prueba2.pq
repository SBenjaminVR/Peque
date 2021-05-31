programa prueba;

mini int factorial(int i) {
    petite int c
    if (i < 0) {
        return 0
    }
    else {
        if (i == 0 || i == 1) {
            c = 1
        }
        else {
            petite int fact
            fact = 1
            while (i > 1) {
                fact = fact * i
                i = i - 1
            }
        }
    }
    if (fact == 1) {
        c = fact
    }
    return c
}



main(){
    print(factorial(5))
}