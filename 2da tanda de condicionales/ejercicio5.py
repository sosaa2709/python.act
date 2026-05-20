print ("Ingresar la temperatura de una bebida (en C°) y se clasificara")
b=int(input())
if b<5:
    print ("Fria")
elif b>=5 and b<=20:
    print ("Templada")
else:
    print ("Caliente")