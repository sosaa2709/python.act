import ttkbootstrap as ttk 
from ttkbootstrap import Messagebox

def saludar():
    nombre=entrada_nombre.get()
    if nombre == "":
        Messagebox.show_error("Ingrese un nombre para poder ejecutar el programa.")
        
    else: 
        resultado.config(text=f"Hola, {nombre}. Bienvenido a ttkbootstrap")

ventana=ttk.Window(themename="darkly")
ventana.title("Mi primer programa con ttkbootstrap")
ventana.geometry("500x300")

ttk.Label(ventana, text="Ingrese su nombre: ").pack(pady=15)

entrada_nombre=ttk.Entry(ventana, width=30)
entrada_nombre.pack(pady=5)

boton_=ttk.Button(ventana, text="Saludar", command=saludar, bootstyle="primary").pack(pady=15)
boton_sal=ttk.Button(ventana, text="Salir", command=ventana.destroy, bootstyle="warning").pack(pady=15)
resultado=ttk.Label(ventana, text="")
resultado.pack(pady=10)

ventana.mainloop()