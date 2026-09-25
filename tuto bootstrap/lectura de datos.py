import ttkbootstrap as ttk 

def mostrar_nombre():
    nombre=entrada.get()
    resultado.config(text="Nombre: " + nombre)

ventana=ttk.Window()
ventana.title("Lectura de datos")
ventana.geometry("500x300")

ttk.Label(ventana, text="Ingrse su nombre: ").pack(pady=10)
entrada=ttk.Entry(ventana)
entrada.pack()

ttk.Button(ventana, text="Mostrar", command=mostrar_nombre).pack(pady="10")

resultado=ttk.Label(ventana, text="")
resultado.pack(pady=10)

ventana.mainloop()