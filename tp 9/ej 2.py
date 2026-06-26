print ("Ingrese la cantidad de segundos y se transformara a minutos y horas")
def minutos(n):
    min=seg/60
    return min

def horas(n):

    hor=seg/3600
    return hor

seg=int(input("Segundos: "))
min=minutos(seg)
hor=horas(seg)

print ("La cantidad de segundos es minutos es: ", min)
print ("La cantidad de segundos en horas es: ", hor)