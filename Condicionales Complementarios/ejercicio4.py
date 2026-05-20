print ("Ingrese la fecha y se determinara cual es el dia siguiente")
d=int(input("Día: "))
m=int(input("Mes: "))
a=int(input("Año: "))
if d>0 and d<30:
    print ("Mañana es: ", d+1, m, a)
elif m>0 and m<12:
    print ("Mañana es: ", 1, m+1, a)
else:
    print ("Mañana es: ", 1, 1, a+1)