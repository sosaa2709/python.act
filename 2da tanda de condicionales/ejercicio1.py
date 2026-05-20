print ("Ingrese la temperatura corporal (C°) y se clasificara")
tem=float(input())
if tem<36:
    print ("Hipotermia")
elif tem>=36 and tem<=37.5:
    print ("Normal")
else:
    print ("Fiebre")