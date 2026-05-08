print ("Ingrese las coordenadas del punto A al punto B se calculara la distancia entre ellos")
AX=float(input("Ingrese la coordenada x del punto A"))
AY=float(input ("Ingrese la coordenada y del punto A"))
BX=float(input("Ingrese la coordenada x del punto B"))
BY=float(input("Ingrese la coordenada y del punto B"))
D=((AX-BX)**2+(AY-BY)**2)**0.5
print("La distancia entre estos dos puntos es:", D)