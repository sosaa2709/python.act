import ttkbootstrap as ttk 
app=ttk.Window(themename="flatly")
app.geometry("700x400")
columnas=("id", "nombre", "apellido")

tabla=ttk.Treeview(app, columns=columnas, show="headings")

tabla.heading("id", text="Documento")
tabla.heading("nombre", text="Nombre")
tabla.heading("apellido", text="Apellido")

tabla.column("id", width=180)
tabla.column("nombre", width=180)
tabla.column("apellido", width=180)

tabla.pack(fill="both", expand=True, padx=20, pady=20)

app.mainloop()