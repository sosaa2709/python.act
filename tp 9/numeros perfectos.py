def es_perfecto(numero):
    suma = 0
    for i in range (1, numero):
        if numero % i == 0:
            suma += i
    return suma == numero
    
num=int(input("Ingrese el numero: "))

if es_perfecto(num):
    print ("Es perfecto")
else:
    print ("No es perfecto.")