def sumar_hasta_n(n):
    suma=0
    for i in range(1, n+1):
        suma += i

    return suma

print ("Hasta que numero queres hacer la suma?")
n=int(input())
if n > 0:
    resultado = sumar_hasta_n(n)
    print ("El resultado es:", resultado)
else:
    print ("Error, debe ingresar un numero positivo")