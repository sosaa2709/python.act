def repetir_palabra (palabra, cantidad):
    for i in range (cantidad):
        print(palabra)

tex=input("Escribe una palabra: ")
cant=int(input("Cuantas veces queres que se repita?: "))
repetir_palabra(tex, cant)