PI=3.1416
print ("Ingrese el radio y la altura de un cilindro para calcular su volumen y area")
RAD=float(input("Radio: "))
ALT=float(input("Altura: "))
VOL=PI*RAD**2*ALT
ARE=2*PI*RAD*(ALT+RAD)
print ("El volumen del cilindro es:", VOL)
print ("El area del cilindro es: ", ARE)