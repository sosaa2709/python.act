def encontrar_max(lista):
    maximo = lista[0]
    for elemento in lista:
        if elemento > maximo:
            maximo = elemento
    return maximo

numeros = []

cantidad=int(input("Cuantos numeros desea ingresar?: "))

for i in range(cantidad):
    numero=int(input(f"Ingrese el numero {i+1}: "))
    numeros.append(numero)

resultado = encontrar_max(numeros)

print ("Los numeros ingresaros fueron: ", numeros)
print ("El maximo de estos es: ", resultado)