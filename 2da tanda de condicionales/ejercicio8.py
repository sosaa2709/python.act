print ("Ingrese las calorias de un alimento y se clasificara")
c=int(input())
if c<100: 
    print ("Ligero")
elif c>=100 and c<=300:
    print ("Moderado")
else: 
    print ("Calórico")