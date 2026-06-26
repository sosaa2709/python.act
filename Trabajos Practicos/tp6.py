positivos=0
negativos=0
ceros=0
for i in range(20):
numero=float(input("Ingrese un numero"))
if numero>0:
    positivos +=1
elif numero<0:
    negativos +=1
else:
    ceros +=1
    
print ("Positivos: ", positivos)
print ("Negativos: ", negativos)
print ("Ceros: ", ceros)