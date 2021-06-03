programa prueba;

mini void bubbleSort() {
    petite int arr[7]
    petite int i, j
    i = 0
    arr[0] = 64
    arr[1] = 34
    arr[2] = 25
    arr[3] = 12
    arr[4] = 22
    arr[5] = 11
    arr[6] = 90

    while (i <> 6) {
        j = 0
        while (j <> 5-i) {
            if (arr[j] > arr[j+1]) {
                petite int aux
                aux = arr[j]
                arr[j] = arr[j+1]
                arr[j+1] = aux
            }

            j = j + 1
        }
        i = i + 1
    }

    i = 0
    for (i to 6, 1) {
        print(arr[i])
        i = i + 1
    }


}
main(){
    bubbleSort()
}