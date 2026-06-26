print ("Ingrese el importe de la compra y si el cliente es asociado (si es asi se le hara un descuento del 10%).")
imp=float(input("Importe: "))
aso=(input ("Es asociado? "))
if aso=="si":
    print ("El precio final es ", imp*0.90)
else:
    print ("El precio final es ", imp)