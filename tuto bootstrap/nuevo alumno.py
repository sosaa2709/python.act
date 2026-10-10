import ttkbootstrap as ttk
from ttkbootstrap import Messagebox
app=ttk.Window(themename="solar")
app.title("Sistema Académido")
app.geometry("700x450")
alumnos_guardados=[]

def nuevo_alum():
    nuev=ttk.Toplevel(app)
    nuev.title("Nuevo Alumno.")
    nuev.geometry("400x260")
    nuev.grab_set()
    ttk.Label(nuev, text="Nombre y apellido: ").pack()
    entry=ttk.Entry(nuev)
    entry.pack()
    opciones= ["1º", "2º", "3º", "4º", "5º", "6º"]
    seleccion=ttk.Combobox(nuev, values=opciones, bootstyle="info")
    seleccion.set("1º")
    seleccion.pack()
    opciones_carrera=("ingenieria", "medicina", "perito", "contaduria")
    carrera_sele=ttk.Combobox(nuev, values=opciones_carrera, bootstyle="info")
    carrera_sele.set("ingenieria")
    carrera_sele.pack()

    def guardar_alumno():
        nombre=entry.get().strip()
        if not nombre:
            entry.focus_set()
            return
        alumnos_guardados.append(f"{nombre} | {seleccion.get()} | {carrera_sele.get()}")
        nuev.destroy()

    def message():
        ttk.Messagebox.yesno("Desea salir?")

    ttk.Button(nuev, text="Salir", command=message).pack()


    ttk.Button(nuev, text="Guardar", command=guardar_alumno, bootstyle="success").pack(pady=10)
    
def alumnos():
    alum=ttk.Toplevel(app)
    alum.title("Alumnos.")
    alum.geometry("400x300")
    alum.grab_set()
    lista=ttk.Listbox(alum, height=10, width=50)
    lista.pack()
    for alumno in alumnos_guardados:
        lista.insert("end", alumno)
    def borrar_alu():
        seleccionados=lista.curselection()
        if seleccionados:
            aluu=seleccionados[0]
            lista.delete(aluu)
            alumnos_guardados.pop(aluu)

    ttk.Button(alum, text="Eliminar alumno", command=borrar_alu, bootstyle="danger").pack(pady=10)
    ttk.Button(alum, text="Salir", command=alum.destroy).pack(pady=10)


def config():
    confi=ttk.Toplevel(app)
    confi.title("Configuracion.")
    confi.geometry("400x200")
    confi.grab_set()

def acerca():
    acer=ttk.Toplevel(app)
    acer.title("Acerca de")
    acer.geometry("400x200")
    acer.grab_set()

ttk.Button(app, text="Alumnos", command=alumnos, bootstyle="primary").pack(pady=13)
ttk.Button(app, text="Nuevo alumno", command=nuevo_alum, bootstyle="secondary").pack(pady=13)
ttk.Button(app, text="Configuracion", command=config, bootstyle="primary").pack(pady=13)
ttk.Button(app, text="Acerca de", command=acerca, bootstyle="secondary").pack(pady=13)
ttk.Button(app, text="Salir", command=app.destroy, bootstyle="warning").pack(pady=13)

app.mainloop()