PPG=3
PPE=1
PPP=0
print ("--------------------------------------")
print("ejercicio 4: puntaje de partido de futbol")
print ("--------------------------------------")
pg=int(input("Ingrese la cantidad de partidos ganados "))
pe=int(input("Ingrese la cantidad de partidos empatados"))
pp=int(input("Ingrese la cantidad de partidos perdidos"))
pf= (PPG*pg)+(PPE*pe)+(PPP*pp)
print("El puntaje final del equipo es: ",pf)