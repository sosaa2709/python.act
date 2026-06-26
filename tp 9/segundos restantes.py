def tiempo(seg):
    horas=seg/3600
    min=seg/60
    segu=(seg%60)
    return horas, min, seg

seg=int(input("Ingrese la cantidad de segundos, estos se pasara a horas y minutos, y se mostraran los segundos restantes: "))
a, b, c=tiempo(seg)
print (a, "horas", b, "minutos", c, "segundos restantes")