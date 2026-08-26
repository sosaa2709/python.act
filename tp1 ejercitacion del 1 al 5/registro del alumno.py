import tkinter as tk 
ventana=tk.Tk()
from tkinter import ttk 
ventana.title("nuevo estudiante")
ventana.geometry("600x300")

etiqueta_nombre=tk.Label(
    ventana, 
    text="Ingrese su nombre y apeliido: "
)
etiqueta_nombre.pack()
entrada_nombre=tk.Entry(ventana)
entrada_nombre.pack()

etiqueta_edad=tk.Label(
    ventana, 
    text="Ingrese su edad: "
)
etiqueta_edad.pack()
entrada_edad=tk.Entry(ventana)
entrada_edad.pack()

def mostrar_datos():
    nombre=entrada_nombre.get()
    edad=entrada_edad.get()
    sexo=sexo_var.get()
    año=año_var.get()
    etiqueta_resultado.config(text=f"{nombre} de {edad} años de edad, de sexo {sexo}, del año {año} ha sido registrado en el sistema.")

etiqueta_resultado=tk.Label(ventana, text="")
etiqueta_resultado.pack()

etiqueta_sexo=tk.Label(ventana, text=("Seleccione el sexo: "))
etiqueta_sexo.pack()

sexo_var=tk.StringVar()
sexo_var.set("Masculino")

tk.Radiobutton(ventana, text="masculino", variable=sexo_var, value="masculino").pack()
tk.Radiobutton(ventana, text="femenino", variable=sexo_var, value="femenino").pack()
tk.Radiobutton(ventana, text="otro", variable=sexo_var, value="otro").pack()

etiqueta_año=tk.Label(ventana, text="Seleccione el año: ").pack()
años= ["1", "2", "3", "4", "5", "6"]
año_var = tk.StringVar()
combo_año = ttk.Combobox(ventana, textvariable=año_var, values=años, state="readonly")
combo_año.set("1")
combo_año.pack()


boton=tk.Button(ventana, text="Mostrar", command=mostrar_datos)
boton.pack()

boton_s=tk.Button(
    ventana,
 text="Salir",
   command=ventana.destroy
)
boton_s.pack()

ventana.mainloop()