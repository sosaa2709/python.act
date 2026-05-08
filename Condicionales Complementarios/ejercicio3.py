PRE=float(input("Ingrese el precio del aparato: "))
IGV=(input("Marca del aparato: "))
if PRE>=2000 and IGV=="NOSY":
    ca= PRE*0.90
    ct= ca*0.95
elif PRE>=2000 and IGV!="NOSY":
    ct= PRE*0.90
elif PRE<2000 and IGV=="NOSY":
    ct=PRE*0.95
elif PRE<2000 and IGV!="NOSY":
    ct=PRE
print ("El precio final del aparato es: ", ct)