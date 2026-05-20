print ("Ingresar ICA y se le dira la calidad del aire")
a=int(input())
if a<50:
    print ("Bueno")
elif a>=50 and a<=100:
    print ("Moderado")
else: 
    print ("Peligroso")