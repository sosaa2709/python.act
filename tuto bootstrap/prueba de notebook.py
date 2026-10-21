import ttkbootstrap as ttk
app=ttk.Window()
app.geometry("800x500")
pestana=ttk.Notebook(app)
columnas=("videojuego", "plataforma", "precio")
Videojuegos=ttk.Frame(app, padding=20)
Agre_juego=ttk.Frame(app, padding=20)
tabla=ttk.Treeview(Videojuegos, columns=columnas, show="headings")
pestana.pack(fill="both", expand=True, padx=20, pady=20)
pestana.add(Videojuegos, text="Videojuegos")
pestana.add(Agre_juego, text="Agregar juegos")

ttk.Label(Agre_juego, text="Ingrese el nombre: ").pack()
entry_vid=ttk.Entry(Agre_juego)
entry_vid.pack()
ttk.Label(Agre_juego, text="Ingrese la plataforma: ").pack()
entry_pla=ttk.Entry(Agre_juego)
entry_pla.pack()
ttk.Label(Agre_juego, text="Ingrese el precio: ").pack()
entry_pre=ttk.Entry(Agre_juego)
entry_pre.pack()


tabla.heading("videojuego", text="Videojuego")
tabla.heading("plataforma", text="Plataforma")
tabla.heading("precio", text="Precio")

tabla.column("videojuego", width=180)
tabla.column("plataforma", width=180)
tabla.column("precio", width=180)

def mostrar():
    nombre=entry_vid.get()
    plataforma=entry_pla.get()
    precio=entry_pre.get()
    if nombre and plataforma and precio:
        tabla.insert("", "end", values=(nombre, plataforma, precio))
        entry_vid.delete(0, "end")
        entry_pla.delete(0, "end")
        entry_pre.delete(0, "end")

ttk.Button(Agre_juego, text="Guardar datos", command=mostrar).pack()


tabla.pack(fill="both", expand=True, padx=20, pady=20)

app.mainloop()