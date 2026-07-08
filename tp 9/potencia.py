def calcular_potencia(base, exponente):
    resultado = 1
    for i in range (exponente):
        resultado *= base
    return resultado
    
bas=int(input("Base: "))
exp=int(input("Exponente: "))

print ("Resultado: ", calcular_potencia(bas, exp))