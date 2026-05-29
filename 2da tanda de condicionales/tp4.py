print("Ingrese la fecha: ")
a = int( input("Año: "))
m = int( input("Mes: "))
d = int( input("Día: "))
#meses de 31 dias
if (m==1 or m==3 or m==5 or m==7 or m==8 or m==10 or m==12) and d<31:
        print ("Mañana es :", d+1, m, a)
elif (m==4 or m==6 or m==9 or m==11) and d<30:
        print ("Mañana es :", d+1, m, a)
elif m==2 and d<29:
        print ("Mañana es: ", 1, m+1, a)
elif m==12:
        print ("Mañana es: ", 1, 1, a+1)
else:
        print ("Mañana es: ", 1, m+1, a)