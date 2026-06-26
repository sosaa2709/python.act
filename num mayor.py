def obtener_mayor(num1, num2):
    if num1>num2:
        return num1
    else:
        return num2
print ("Escriba dos numeros y se determinara cual es el mayor")
num1=int(input())
num2=int(input())
num=obtener_mayor(num1, num2)
print ("El numero mayor es ", num)