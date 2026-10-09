import ttkbootstrap as ttk
from ttkbootstrap import Messagebox
import winsound

def presenat():
    nombre=entrada_nombre.get()
    apellido=entrada_apellido.get()
    curso=seleccion.get()
    carrera=carrera_sele.get()
    if nombre=="" or apellido=="":
        Messagebox.show_error("Ingrese un nombre y apellido valido bro🥀", "⚠️⚠️⚠️error⚠️⚠️⚠️")
        winsound.Beep(800, 500)
    else:
        resultado.config(text=f"hola {nombre} {apellido} de {curso}. bienvenido al sistema\n escolar de {carrera}")

ventana=ttk.Window(themename="solar")
ventana.title("Mi primer programa con ttkbootstrap")
ventana.geometry("650x450")
ttk.Label(ventana, text="Ingrese su nombre:", bootstyle="secondary").pack(pady=15)
entrada_nombre=ttk.Entry(ventana, width=30, bootstyle="primary")
entrada_nombre.pack(pady=5)
ttk.Label(ventana, text="Ingrese su apellido:", bootstyle="secondary").pack(pady=15)
entrada_apellido=ttk.Entry(ventana,width=30,bootstyle="primary")
entrada_apellido.pack(pady=5)
opciones= ["1º", "2º", "3º", "4º", "5º", "6º"]
seleccion=ttk.Combobox(ventana, values=opciones, bootstyle="info")
seleccion.set("1º")
seleccion.pack()
opciones_carrera=("ingenieria", "medicina", "perito", "contaduria")
carrera_sele=ttk.Combobox(ventana, values=opciones_carrera, bootstyle="info")
carrera_sele.set("ingenieria")
carrera_sele.pack()
saludadad=ttk.Button(ventana, text="SALUDAR", command=presenat, bootstyle="primary").pack(pady=15)

resultado=ttk.Label(ventana, text="", bootstyle="success")
resultado.pack(pady=10)
boton=ttk.Button(ventana, text="salir", command=ventana.destroy, bootstyle="warning")
boton.pack(pady=10)
ventana.mainloop()