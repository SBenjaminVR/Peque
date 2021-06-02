programa prueba;

main() {
    petite int i
    petite list int listaMagica
    listaMagica->append(64)
    listaMagica->append(34)
    listaMagica->append(25)
    listaMagica->append(12)
    listaMagica->append(22)
    listaMagica->append(11)
    listaMagica->append(60)

    print("ESTE ES EL HEAD")
    print(listaMagica->head())
    print("ESTE ES EL TAIL")
    print(listaMagica->tail())

    listaMagica->append(20000)
    listaMagica->append(40000)
    listaMagica->pop()
    listaMagica->pop()

    listaMagica->sort()

    print("ESTE ES EL LA POSICION DEL 34")
    print(listaMagica->find(34))

    i = 0
    print("AHI VIENE LA LISTA EN ORDEN")
    for (0 to 6, 1) {
        print(listaMagica->key(i))
        i = i + 1
    }
}