import ttkbootstrap as ttk
from ttkbootstrap import Messagebox
app=ttk.Window()
app.title("Abrir dialogo")
app.geometry("600x400")

label=ttk.Label(app, text="Apriete el siguiente boton para continuar: ").pack(pady=30)

def abrir_dialogo():
    dialogo=ttk.Toplevel(app)
    dialogo.title("Confirmacion")
    dialogo.geometry("200x100")

    dialogo.transient(app)
    dialogo.grab_set()

    label=ttk.Label(dialogo, text="Deseas continuar?").pack(pady=15)

    def cerrar():
        dialogo.grab_release()
        dialogo.destroy()

    boton=ttk.Button(dialogo, text="Aceptar.", command=cerrar).pack(pady=10)

boton=ttk.Button(app, text="Abrir dialogo", command=abrir_dialogo).pack(pady=10)

boton=ttk.Button(app, text="Cerrar", command=app.destroy).pack()

app.mainloop()