import ttkbootstrap as ttk
from ttkbootstrap import Messagebox
app=ttk.Window(themename="solar")
app.title("Sistema Académido.")
app.geometry("500x280")
alumnos_guardados=[]

bienvenida = ttk.Label(app, text="Bienvenido al sistema de gestion.", anchor="w", font=("Segoe UI", 16, "bold"))
bienvenida.pack(fill="x", padx=10, pady=(10, 12))

def nuevo_alum():
    nuev=ttk.Toplevel(app)
    nuev.title("Nuevo Alumno.")
    nuev.geometry("400x260")
    nuev.grab_set()
    ttk.Label(nuev, text="Nombre y apellido: ").pack()
    entry=ttk.Entry(nuev)
    entry.pack()
    ttk.Label(nuev, text="Año:").pack()
    opciones= ["1º", "2º", "3º", "4º", "5º", "6º"]
    seleccion=ttk.Combobox(nuev, values=opciones, bootstyle="info", state="readonly")
    seleccion.set("1º")
    seleccion.pack()
    ttk.Label(nuev,text="Carrera:").pack()
    opciones_carrera=("Ingenieria", "Medicina", "Perito", "Contaduria")
    carrera_sele=ttk.Combobox(nuev, values=opciones_carrera, bootstyle="info", state="readonly")
    carrera_sele.set("ingenieria")

    carrera_sele.pack()
    def guardar_alumno():
        nombre=entry.get().strip()
        if not nombre:
            Messagebox.show_error("Completa el nombre y apellido del alumno.", title="Campo obligatorio", parent=nuev)
            entry.focus_set()
            return
        alumnos_guardados.append(f"{nombre} | {seleccion.get()} | {carrera_sele.get()}")
        nuev.destroy()

    def message():
        respuesta=Messagebox.yesno("Desea salir?", text="Confirmar salida?", parent=nuev)
        if respuesta == "Yes":
            nuev.destroy()
        
    ttk.Button(nuev, text="Guardar", command=guardar_alumno, bootstyle="success").pack(pady=10)
    ttk.Button(nuev, text="Salir", command=message, bootstyle="warning").pack(pady=10)
    
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
            indice=seleccionados[0]
            lista.delete(indice)
            alumnos_guardados.pop(indice)
            if not alumnos_guardados:
                boton_borrar.pack_forget()

    boton_borrar=ttk.Button(alum, text="Eliminar alumno", command=borrar_alu, bootstyle="dark")
    if alumnos_guardados:
        boton_borrar.pack(pady=10)
    def message():
        respuesta=Messagebox.yesno("Desea salir?", text="Confirmar salida?", parent=alum)
        if respuesta == "Yes":
           alum.destroy()
           
   
    ttk.Button(alum, text="Salir", command=message, bootstyle="warning").pack(pady=10)

def acerca():
    acer=ttk.Toplevel(app)
    acer.title("Acerca de")
    acer.geometry("400x200")
    acer.grab_set()
    ttk.Label(acer, text='Nombre del programa: "Nuevo alumno de IMCO".').pack(pady=10)
    ttk.Label(acer, text="Nombre del autor: Lautaro Sosa.").pack(pady=10)
    ttk.Label(acer, text="Version: 1.18").pack(pady=10)
    ttk.Label(acer, text="Año: 2026").pack(pady=10)
    def message():
        respuesta=Messagebox.yesno("Desea salir?", text="Confirmar salida?",  parent=acer, )
        if respuesta == "Yes":
            acer.destroy()
    ttk.Button(acer, text="Salir",command=message, bootstyle="warning").pack(pady=8)

def config():
    confi=ttk.Toplevel(app)
    confi.title("Configuración.")
    confi.geometry("400x200")
    confi.grab_set()
    ttk.Label(confi, text="Ingrese el nombre de usuario").pack()
    entry=ttk.Entry(confi)
    entry.pack()
    def aceptar():
        usuario=entry.get().strip()
        if not usuario:
            Messagebox.show_error("Ingrese el nombre de usuario para continuar.", title="Campo obligatorio", parent=confi)
            entry.focus_set()
            return

        bienvenida.config(text=f"Bienvenido al sistema de gestion, {usuario}.")
        Messagebox.show_info(f"Configuracion guardada para {usuario}", title="Configuración", parent=confi)
        confi.destroy()

    botones=ttk.Frame(confi)
    botones.pack()

    ttk.Button(botones, text="Aceptar", bootstyle="success", command=aceptar).pack(side="left", padx=5, pady=10)
    ttk.Button(botones, text="Cancelar", bootstyle="success", command=confi.destroy).pack(side="right", padx=5, pady=10)
    def message():
            respuesta=Messagebox.yesno("Desea salir?", text="Confirmar salida?", parent=confi)
            if respuesta == "Yes":
               confi.destroy()
    ttk.Button(confi, text="Salir", bootstyle="warning", command=message).pack(pady=10)

ttk.Button(app, text="Alumnos", command=alumnos, bootstyle="secondary").pack(fill="x", padx=30, pady=4)
ttk.Button(app, text="Nuevo alumno", command=nuevo_alum, bootstyle="secondary").pack(fill="x", padx=30, pady=4)
ttk.Button(app, text="Acerca de", command=acerca, bootstyle="secondary").pack(fill="x", padx=30, pady=4)
ttk.Button(app, text="Configuración", command=config, bootstyle="secondary").pack(fill="x", padx=30, pady=4)

def message():
    respuesta=Messagebox.yesno("Desea salir?", text="Confirmar salida?",  parent=app, )
    if respuesta == "Yes":
        app.destroy()
        

ttk.Button(app, text="Salir", command=message, bootstyle="warning").pack(fill="x", padx=30, pady=4)

app.mainloop()