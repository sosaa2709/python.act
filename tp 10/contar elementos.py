def contar_ele (lista):
    suma = 0
    for elemento in lista:
        suma += 1
    return suma 

numeros = []

cantidad=int(input("Ingrese la cantidad de numeros que se podran poner en la lista: "))

for i in range(cantidad):
    numero=int(input(f"Ingrese el numero {i+1}: "))
    numeros.append(numero)

resultado = contar_ele(numeros)

print ("Los numeros ingresados fueron: ", numeros)
print ("La cantidad de elementos es: ", resultado)
