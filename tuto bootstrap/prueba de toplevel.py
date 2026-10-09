import ttkbootstrap as ttk 

app=ttk.Window(themename="darkly")
app.title("Ventana principal")
app.geometry("500x300")

def abrir_ventana():
    ventana=ttk.Toplevel(app)
    ventana.title("Ventana secundaria")
    ventana.geometry("400x250")

    ttk.Label(ventana, text="Ingrese sus datos ").pack(pady=40)

    ttk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=50)

ttk.Label(app, text="Presione el siguiente boton para abrir la 2da ventana.").pack()

ttk.Button(app, text="Abrir ventana", command=abrir_ventana).pack(pady=50)

ttk.Button(app, text="Cerrar", command=app.destroy).pack(pady=50)

app.mainloop()