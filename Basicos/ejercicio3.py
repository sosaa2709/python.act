PRC=3
PRI=-1
PRB=0
print("-------------------------------")
print("Ejercicio 3: puntaje en examen")
print("-------------------------------")
RC=int(input("Ingrese el numero de respuestas correctas"))
RI=int(input("Ingrese el numero de respuestas incorrectas"))
RB=int(input("Ingrese el numero de respuestas en blanco"))
PF=PRC*RC+PRI*RI+PRB*RB
print("El puntaje final del examen es:",PF)
