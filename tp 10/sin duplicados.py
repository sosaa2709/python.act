def eliminar_duplicados(lista):
    lista_sin_duplicados = []
    for elemento in lista:
        if elemento not in lista_sin_duplicados:
            lista_sin_duplicados.append(elemento)
    return lista_sin_duplicados

original = [1, 2, 2, 3, 4, 4, 5]
sin_duplicados = eliminar_duplicados(original)
print (sin_duplicados)