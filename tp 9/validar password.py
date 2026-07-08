def validar_password(password):
    return len(password) >=8

clave = input ("Ingrese la contraseña: ")

if validar_password(clave):
    print ("Contraseña valida.")
else:
    print ("La contraseña debe tener al menos 8 caracteres.")