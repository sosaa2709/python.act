import tkinter as tk 
ventana=tk.Tk()
from tkinter import messagebox
ventana.title("reserva de fiestas")
ventana.geometry("600x300")

etiqueta_nombre(ventana, text="Ingrese el nombre: ").pack()
entrada_nombre=tk.Entry(ventana)
entrada_nombre.pack()

etiqueta_invitados(ventana, text="Ingrese la cantidad de invitados: ").pack()
entrada_invitados=tk.Entry(ventana)
entrada_nombre.pack()

etiqueta_evento(ventana, text="Seleccione el tipo de evento: ").pack()

evento_var=tk.StringVar()
evento_var.set("Cumpleaños")

tk.Radiobutton(ventana, text="Cumpleaños", variable=evento_var, value="Cumpleaños")
tk.Radiobutton(ventana, text="Casamiento", variable=evento_var, value="Casamiento")
tk.Radiobutton(ventana, text="Empresarial", variable=evento_var, value="Empresarial")

dj_var=tk.BooleanVar()
cathering=tk.BooleanVar()
fotografia=tk.BooleanVar()

tk.Checkbutton(ventana, text="DJ y sonido ($40.000)", variable=dj_var).pack()
tk.Checkbutton(ventana, text="Cathering / Comida($80.000)", variable=cathering).pack()
tk.Checkbutton(ventana, text="Fotografia($30.000)", variable=fotografia).pack()

resultado=tk.Label(ventana, text="").pack

def calc():
    try:
        invitados=int(entrada_invitados.get())
        precio = 2000
        subtotal= precio x invitados
