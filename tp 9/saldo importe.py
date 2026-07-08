def extraer_saldo(sal, imp):
    return imp <= sal

sal=float(input("Saldo disponible: "))
imp=float(input("Importe a retirar: "))

if extraer_saldo (sal, imp):
    print ("Operacion exitosa.")
else:
    print ("Salado insuficiente.")