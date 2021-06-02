programa prueba;

mini int pruebaInput() {
    petite int b[3][3]
    input(b[0][0])
    return b[0][0]
}

main() {
    petite int matrizA[3][3]
    petite int matrizB[3][3]
    petite int matrizC[3][3]
    petite int i, j
    
    i = 0
    j = 0
    for (i to 2, 1) {
        for (j to 2, 1) {
            matrizA[i][j] = i * j
            matrizB[i][j] = i + j
            matrizC[i][j] = matrizA[i][j] * matrizB[i][j]
            j = j + 1
        }
        i = i + 1
        j = 0
    }
    print(matrizA[2][1])
    print(matrizB[2][1])
    print(matrizC[2][1])
}