import tkinter as tk 
ventana=tk.Tk()
from tkinter import messagebox
ventana.title("reserva de fiestas")
ventana.geometry("600x300")

etiqueta_nombre=tk.Label(ventana, text="Ingrese el nombre: ").pack()
entrada_nombre=tk.Entry(ventana)
entrada_nombre.pack()

etiqueta_invitados=tk.Label(ventana, text="Ingrese la cantidad de invitados: ").pack()
entrada_invitados=tk.Entry(ventana)
entrada_invitados.pack()

etiqueta_evento=tk.Label(ventana, text="Seleccione el tipo de evento: ").pack()

evento_var=tk.StringVar()
evento_var.set("Cumpleaños")

tk.Radiobutton(ventana, text="Cumpleaños", variable=evento_var, value="Cumpleaños").pack()
tk.Radiobutton(ventana, text="Casamiento", variable=evento_var, value="Casamiento").pack()
tk.Radiobutton(ventana, text="Empresarial", variable=evento_var, value="Empresarial").pack()

dj_var=tk.BooleanVar()
cathering=tk.BooleanVar()
fotografia=tk.BooleanVar()

tk.Checkbutton(ventana, text="DJ y sonido ($40.000)", variable=dj_var).pack()
tk.Checkbutton(ventana, text="Cathering / Comida($80.000)", variable=cathering).pack()
tk.Checkbutton(ventana, text="Fotografia($30.000)", variable=fotografia).pack()

resultado=tk.Label(ventana, text="")
resultado.pack()

def calc():
    try:
        invitados=int(entrada_invitados.get())
    except ValueError:
        messagebox.showerror("Error.", "Complete el nombre y use valores positivos.")
        return
    subtotal = 2000*invitados
    servicio=0
    if dj_var.get():
        servicio=+40000
    if cathering.get():
        servicio=+80000
    if fotografia.get():
        servicio=+30000

    total=subtotal+servicio

    if total > 100:
        descuento = total * 0.15
        total_final = total - descuento
        resultado.config(
            text=f"El total es: ${total_final:,.0f} (descuento aplicado: ${descuento:,.0f})"
        )
    else:
        resultado.config(text=f"El total es: ${total:,.0f}")

boton=tk.Button(ventana, text="Calcular", command=calc).pack()
boton_s=tk.Button(ventana, text="Salir", command=ventana.destroy).pack()

ventana.mainloop()