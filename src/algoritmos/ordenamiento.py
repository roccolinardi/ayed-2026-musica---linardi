def ordenar_seleccion(coleccion, clave):
    """Ordenamiento por selección. Devuelve una nueva secuencia, no usa sorted."""
    resultado = list(coleccion)
    n = len(resultado)

    for i in range(n - 1):
        idx_min = i
        for j in range(i + 1, n):
            if clave(resultado[j]) < clave(resultado[idx_min]):
                idx_min = j
        if idx_min != i:
            resultado[i], resultado[idx_min] = resultado[idx_min], resultado[i]

    return resultado


def ordenar_insercion(coleccion, clave):
    """Ordenamiento por inserción. Devuelve una nueva secuencia, no usa sorted."""
    resultado = list(coleccion)
    n = len(resultado)

    for i in range(1, n):
        actual = resultado[i]
        clave_actual = clave(actual)
        j = i - 1

        while j >= 0 and clave(resultado[j]) > clave_actual:
            resultado[j + 1] = resultado[j]
            j -= 1

        resultado[j + 1] = actual

    return resultado