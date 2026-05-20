print ("Ingrese el porcentaje de la bateria y se clasificara")
b=int(input("%"))
if b==100:
    print ("La bateria esta completa")
elif b>=20 and b<=99:
    print ("La bateria es adecuada")
else: 
    print ("La bateria es baja")