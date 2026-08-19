import tkinter as tk
ventana=tk.Tk()
ventana.title("Saludo personalizado")
ventana.geometry("450x250")

etiqueta_nombre=tk.Label(ventana, text="Ingrese su nombre: ")
etiqueta_nombre.pack()
entrada_nombre=tk.Entry(ventana)
entrada_nombre.pack()

etiqueta_apellido=tk.Label(ventana, text="Ingrese su apellido: ")
etiqueta_apellido.pack()
entrada_apellido=tk.Entry(ventana)
entrada_apellido.pack()

def mostrar_na():
    nombre=entrada_nombre.get()
    apellido=entrada_apellido.get()
    nombre_resul = f"{nombre} {apellido}"
    etiqueta_resultado.config(text=f"Hola {nombre_resul} ")

boton=tk.Button(ventana, text="Mostrar", command=mostrar_na)
boton.pack()

etiqueta_resultado=tk.Label(ventana, text="")
etiqueta_resultado.pack()

boton2=tk.Button(ventana, text="Salir", command=ventana.destroy)
boton2.pack()

ventana.mainloop()