import ttkbootstrap as ttk 
from ttkbootstrap import Messagebox

def presentar():
    nombre=entrada_nombre.get()
    apellido=entrada_apellido.get()
    año=año_var.get()
    carrera=carrera_var.get()
    if nombre == "" or apellido == "" or año == "" or carrera == "":
        Messagebox.show_error("Complete todo.")
    else:
        resultado.config(f"Nombre: {nombre} {apellido}\n" f"Año:  {año}\n" f"Carrera: {carrera}")

ventana=ttk.Window(themename="darkly")
ventana.title("Mi primer programa con ttkbootstrap")
ventana.geometry("500x300")

ttk.Label(ventana, text="Formulario de presentacion").pack(pady=15)
ttk.Label(ventana, text="Nombre: ").pack()
entrada_nombre=ttk.Entry(ventana, width=35)
entrada_nombre.pack(pady=5)
ttk.Label(ventana, text="Apellido: ").pack()
entrada_apellido=ttk.Entry(ventana, width=35)
entrada_apellido.pack(pady=5)

etiqueta_año=ttk.Label(ventana, text="Seleccione el año: ").pack()
años= ["1", "2", "3", "4", "5", "6"]
año_var = ttk.StringVar()
combo_año = ttk.Combobox(ventana, textvariable=año_var, values=años, state="readonly")
combo_año.set("1")
combo_año.pack()

etiqueta_año=ttk.Label(ventana, text="Seleccione la carrera: ").pack()
carrera= ["Derecho", "Ingenieria", "Medicina", "Psicologia"]
carrera_var = ttk.StringVar()
combo_carrera = ttk.Combobox(ventana, textvariable=año_var, values=años, state="readonly")
combo_carrera.set("1")
combo_carrera.pack()

ttk.Button(ventana, text="Generar presentacion", command=presentar, bootstyle="succes").pack(pady=15)

resultado=ttk.Label(ventana, text="")
resultado.pack(pady=10)

ventana.mainloop()