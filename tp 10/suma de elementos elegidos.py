def suma_num(lista):
    suma = 0
    for elemento in lista:
        suma += elemento
    return suma

numeros = []

cantidad=int(input("Cuantos numeros desea ingresar?: "))

for i in range(cantidad):
    numero=int(input(f"Ingrese el numero {i+1}: "))
    numeros(numero)

resultado = suma_num(numeros)

print ("Los numeros ingresados fueron: ", numeros)
print ("La suma de estos numeros es: ", resultado)