import ttkbootstrap as ttk 

ventana=ttk.Window()
ventana.title("Mi primera aplicacion.")
ventana.geometry("500x300")

etiqueta_nombre=ttk.Label(ventana, text="Ingrese su nombre")
etiqueta_nombre.pack()
entrada_nombre=ttk.Entry(ventana)
entrada_nombre.pack()

def saludar():
    nombre=entrada_nombre.get()
    if nombre=="":
        resultado.config(text="Error")
    else:
        resultado.config(text=f"Hola {nombre}")

resultado=ttk.Label(ventana, text="")
resultado.pack()

boton=ttk.Button(ventana, text="Saludar", command=saludar, bootstyle="primary")
boton.pack()

ventana.mainloop()