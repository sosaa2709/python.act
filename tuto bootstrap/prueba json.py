import json  
from pathlib import Path  
import ttkbootstrap as ttk  
from ttkbootstrap import Messagebox

ARCHIVO = Path("alumnos.json")
ARCHIVO_CONFIG = Path(__file__).with_name("configuracion.json")
app=ttk.Window(themename="solar")
app.title("Sistema Académido.")
app.geometry("500x280")

def cargar_alumnos():
    if not ARCHIVO.exists():
        return []
    try:
        with ARCHIVO.open("r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        if not isinstance(datos, list):
            raise ValueError("El JSON debe contener una lista de alumnos.")
        return datos
    except (json.JSONDecodeError, OSError, ValueError) as error:
        Messagebox.show_error(
            f"No se pudieron cargar los alumnos.\n{error}",
            title="Error al cargar",
            parent=app,
        )
        return []


def guardar_alumnos():
    try:
        with ARCHIVO.open("w", encoding="utf-8") as archivo:
            json.dump(alumnos_guardados, archivo, indent=4, ensure_ascii=False)
        return True
    except OSError as error:
        Messagebox.show_error(
            f"No se pudieron guardar los alumnos.\n{error}",
            title="Error al guardar",
            parent=app,
        )
        return False


alumnos_guardados = cargar_alumnos()


def cargar_configuracion():
    if not ARCHIVO_CONFIG.exists():
        return {}
    try:
        with ARCHIVO_CONFIG.open("r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        if not isinstance(datos, dict):
            raise ValueError("La configuración debe ser un objeto JSON.")
        return datos
    except (json.JSONDecodeError, OSError, ValueError) as error:
        Messagebox.show_error(
            f"No se pudo cargar la configuración.\n{error}",
            title="Error de configuración",
            parent=app,
        )
        return {}


def guardar_configuracion(datos):
    try:
        with ARCHIVO_CONFIG.open("w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        return True
    except OSError as error:
        Messagebox.show_error(
            f"No se pudo guardar la configuración.\n{error}",
            title="Error de configuración",
            parent=app,
        )
        return False


configuracion = cargar_configuracion()
if not isinstance(configuracion.get("usuario", ""), str):
    configuracion["usuario"] = ""

bienvenida = ttk.Label(
    app,
    text=f"Bienvenido al sistema de gestion, {configuracion['usuario']}." if configuracion.get("usuario") else "Bienvenido al sistema de gestion.",
    anchor="w",
    font=("Segoe UI", 16, "bold"),
)
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
    carrera_sele.set("Ingenieria")

    carrera_sele.pack()
    def guardar_alumno():
        nombre=entry.get().strip()
        if not nombre:
            Messagebox.show_error("Completa el nombre y apellido del alumno.", title="Campo obligatorio", parent=nuev)
            entry.focus_set()
            return
        alumno = {
            "nombre": nombre,
            "anio": seleccion.get(),
            "carrera": carrera_sele.get(),
        }
        alumnos_guardados.append(alumno)
        if guardar_alumnos():
            nuev.destroy()
        else:
            alumnos_guardados.pop()

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
        lista.insert(
            "end",
            f"{alumno['nombre']} | {alumno['anio']} | {alumno['carrera']}",
        )
    def borrar_alu():
        seleccionados=lista.curselection()
        if seleccionados:
            indice=seleccionados[0]
            alumno_eliminado = alumnos_guardados.pop(indice)
            if not guardar_alumnos():
                alumnos_guardados.insert(indice, alumno_eliminado)
                return
            lista.delete(indice)
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
    entry.insert(0, configuracion.get("usuario", ""))
    def aceptar():
        usuario=entry.get().strip()
        if not usuario:
            Messagebox.show_error("Ingrese el nombre de usuario para continuar.", title="Campo obligatorio", parent=confi)
            entry.focus_set()
            return

        if guardar_configuracion({"usuario": usuario}):
            configuracion["usuario"] = usuario
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