def suma_num(lista):
    suma = 0
    for elemento in lista:
        suma += elemento 
    return suma

#Ingresar que numeros se quiere sumar
numeros = (20, 20, 20, 20, 20)
resultado = suma_num(numeros)
print ("La suma de esta lista de numeros es: ", resultado)