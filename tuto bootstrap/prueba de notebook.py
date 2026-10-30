import json
from pathlib import Path
from tkinter import messagebox
import ttkbootstrap as ttk

app=ttk.Window(themename="solar")
app.geometry("800x500")
app.minsize(650, 400)
app.title("Biblioteca de videojuegos")
pestana=ttk.Notebook(app)
columnas=("videojuego", "plataforma", "precio")
ARCHIVO=Path(__file__).with_name("videojuegos.json")

def cargar_videojuegos():
    if not ARCHIVO.exists():
        return []
    try:
        with ARCHIVO.open("r", encoding="utf-8") as archivo:
            datos=json.load(archivo)
        if not isinstance(datos, list) or any(
            not isinstance(juego, dict)
            or any(not isinstance(juego.get(campo), str) for campo in columnas)
            for juego in datos
        ):
            raise ValueError("El archivo debe contener una lista de videojuegos valida.")
        return datos
    except (json.JSONDecodeError, OSError, ValueError) as error:
        messagebox.showerror(
            "Error al cargar",
            f"No se pudieron cargar los videojuegos.\n{error}",
            parent=app,
        )
        return []


def guardar_videojuegos():
    try:
        with ARCHIVO.open("w", encoding="utf-8") as archivo:
            json.dump(videojuegos_guardados, archivo, indent=4, ensure_ascii=False)
        return True
    except OSError as error:
        messagebox.showerror(
            "Error al guardar",
            f"No se pudieron guardar los videojuegos.\n{error}",
            parent=app,
        )
        return False


videojuegos_guardados=cargar_videojuegos()
Videojuegos=ttk.Frame(app, padding=20)
Agre_juego=ttk.Frame(app, padding=20)
tabla=ttk.Treeview(Videojuegos, columns=columnas, show="headings")
pestana.pack(fill="both", expand=True, padx=20, pady=20)
pestana.add(Videojuegos, text="Videojuegos")
pestana.add(Agre_juego, text="Agregar juegos")

ttk.Label(Videojuegos, text="Biblioteca de videojuegos", font=("Segoe UI", 18, "bold"), bootstyle="primary").pack(anchor="w", padx=20, pady=(8, 0))
ttk.Label(Videojuegos, text="Tus juegos guardados", bootstyle="secondary").pack(anchor="w", padx=20, pady=(2, 12))

ttk.Label(Agre_juego, text="Agregar un videojuego", font=("Segoe UI", 18, "bold"), bootstyle="primary").grid(row=0, column=0, columnspan=2, sticky="w", pady=(8, 20))
Agre_juego.columnconfigure(1, weight=1)

ttk.Label(Agre_juego, text="Nombre del videojuego").grid(row=1, column=0, sticky="e", padx=(0, 14), pady=8)
entry_vid=ttk.Entry(Agre_juego)
entry_vid.grid(row=1, column=1, sticky="ew", pady=8)
ttk.Label(Agre_juego, text="Plataforma").grid(row=2, column=0, sticky="e", padx=(0, 14), pady=8)
entry_pla=ttk.Entry(Agre_juego)
entry_pla.grid(row=2, column=1, sticky="ew", pady=8)
ttk.Label(Agre_juego, text="Precio").grid(row=3, column=0, sticky="e", padx=(0, 14), pady=8)
entry_pre=ttk.Entry(Agre_juego)
entry_pre.grid(row=3, column=1, sticky="ew", pady=8)


tabla.heading("videojuego", text="Videojuego", anchor="center")
tabla.heading("plataforma", text="Plataforma", anchor="center")
tabla.heading("precio", text="Precio", anchor="center")

tabla.column("videojuego", width=260, anchor="center", stretch=True)
tabla.column("plataforma", width=200, anchor="center", stretch=True)
tabla.column("precio", width=150, anchor="center", stretch=True)

for juego in videojuegos_guardados:
    tabla.insert("", "end", values=tuple(juego[campo] for campo in columnas))

def mostrar():
    nombre=entry_vid.get().strip()
    plataforma=entry_pla.get().strip()
    precio=entry_pre.get().strip()
    if not nombre or not plataforma or not precio:
        messagebox.showwarning("Datos incompletos", "Completa todos los campos.", parent=app)
        return

    juego={"videojuego": nombre, "plataforma": plataforma, "precio": precio}
    videojuegos_guardados.append(juego)
    if guardar_videojuegos():
        tabla.insert("", "end", values=tuple(juego[campo] for campo in columnas))
        entry_vid.delete(0, "end")
        entry_pla.delete(0, "end")
        entry_pre.delete(0, "end")
    else:
        videojuegos_guardados.pop()

ttk.Button(Agre_juego, text="Guardar videojuego", command=mostrar, bootstyle="success").grid(row=4, column=1, sticky="e", pady=(18, 8))


tabla.pack(fill="both", expand=True, padx=20, pady=(8, 20))

app.mainloop()