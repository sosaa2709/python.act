def encontrasr_max(lista):
    maximo = lista[0]
    for elemento in lista:
        if elemento > maximo:
            maximo = elemento
    return maximo

numeros = (34, 54, 67, 12, 21)
resultado = encontrasr_max(numeros)
print ("El numero mayor es: ", resultado)