def ordenar_lista(lista):
    return sorted(lista)

numeros = []

cantidad=int(input("Ingrese la cantidad de numeros que podra tener la lista: "))

for i in range(cantidad):
    numero=int(input(f"Ingrese el numero {i+1}: "))
    numeros.append(numero)

ordenados = ordenar_lista(numeros)

print ("Los numeros ingresados fueron: ", numeros)
print ("La lista ordenada es: ", ordenados)