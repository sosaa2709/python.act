MD=1.44
print ("--------------------------------------")
print ("Ejercicio 5: Numero de Micro Discos 3.5 necesarios para almacenar 1 GB")
print ("--------------------------------------")
print ("Ingrese la cantidad de GB de la copia de seguridad para saber cuantos MD se necesitan")
GB=int(input("Ingrese la cantidad de GB: "))
MB=GB*1024
MDN=MB/MD
print("Se necesitan ", MDN, " micro discos de 3.5 para almacenar ", GB, " GB")