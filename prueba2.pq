programa prueba;

peque animal {
    petite int clasificacion

    mini float resta(float b) {
        return b - clasificacion
    }
}

peque canino agranda animal {
    petite int nombre

    mini float suma(float a) {
        petite list int facha
        facha->append(3)
        facha->append(1)
        facha->append(2)
        facha->append(5)
        facha->append(4)
        facha->append(6)
        print(facha->key(1))
        return a + nombre + clasificacion
    }
}

main() {
    petite float zury
    perro = new canino
    camaleon = new animal
    perro.nombre = 2
    perro.clasificacion = 3
    input(perro.nombre)
    zury = perro.suma(5.0)
    camaleon.clasificacion = 6
    print(zury)
    print(camaleon.resta(3.0))

}