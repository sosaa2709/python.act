def convertir_tiempo(segundos):
    horas = segundos // 3600
    minutos = (segundos%3600) // 60
    segundos_restantes = segundos % 60
    return horas, minutos, segundos_restantes

seg = int(input("Ingrese la cantidad de segundos: "))
h, m, s = convertir_tiempo(seg)
print(f"{h} horas, {m} minutos, {s} segundos")