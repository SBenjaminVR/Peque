programa prueba;

# Funcion que te dice en que lugar del arreglo esta el numero
mini int find(int number) {
    petite int a[50]
    petite int i, j, lugar
    i = 49
    j = 0
    lugar = -1
    while (i >= 0) {
        a[i] = j
        j = j + 1
        i = i - 1
    }
    i = 0
    while(i < 50) {
        if (a[i] == number) {
            lugar = i
        }
        i = i + 1
    }
    return lugar
}
main(){
    print(find(2 * 3 + 3))
}