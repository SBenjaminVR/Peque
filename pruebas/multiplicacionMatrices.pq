programa prueba;

mini void multiplicacionMatrices() {
    petite int matrizA[3][3]
    petite int matrizB[3][3]
    petite int matrizC[3][3]
    petite int i, j, k, aux, aux2
    i = 0

    # Llenado de matrices a y b
    for (0 to 2, 1) {
        j = 0
        for (0 to 2, 1) {
            matrizC[i][j] = 0
            # matrizA[i][j] = i + j
            # matrizB[i][j] = i * j
            
            j = j + 1
        }
        i = i + 1
    }

    i = 0
    for (0 to 2, 1) {
        j = 0
        for (0 to 2, 1) {
            k = 0
            for (0 to 2, 1) {
                k = k + 1
            }
            j = j + 1
        }
        i = i + 1
    }

    print("IMPRESOR")
    #Impresor de matriz
    i = 0
    for (0 to 2, 1) {
        j = 0
        for (0 to 2, 1) {
            print(matrizC[i][j])
            j = j + 1
        }
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        i = i + 1
    }

}
main(){
    multiplicacionMatrices()
}