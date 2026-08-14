import tkinter as tk

ventana=tk.Tk()
ventana.title("Ingreso de datos")
ventana.geometry("400x250")

etiqueta_nombre=tk.Label(
    ventana,
    text="Ingrese su nombre"
)
etiqueta_nombre.pack()

entrada_nombre=tk.Entry(ventana)
entrada_nombre.pack()

def mostrar_nombre():
    nombre=entrada_nombre.get()
    resultado.config(
        text="Hola" + nombre
    )

boton=tk.Button(
    ventana,
    text="Mostrar",
    command=mostrar_nombre
)
boton.pack()

resultado=tk.Label(
    ventana,
    text=""
)

ventana.mainloop()