def eliminar_duplicados(lista):
    lista_sin_duplicados = []
    for elemento in lista:
        if elemento not in lista_sin_duplicados:
            lista_sin_duplicados.append(elemento)
    return lista_sin_duplicados

original = []

cantidad=int(input("Ingrese la cantidad de numeros que puede tener la lista: "))

for i in range(cantidad):
    numero=int(input(f"Ingrese el numero {i+1}: "))
    original.append(numero)

sin_duplicados = eliminar_duplicados(original)

print ("Los numeros ingresados fueron: ", original)
print ("La lista sin los duplicados es: ", sin_duplicados)