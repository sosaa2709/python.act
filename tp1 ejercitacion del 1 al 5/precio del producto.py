import tkinter as tk 
ventana=tk.Tk()
from tkinter import messagebox
ventana.title("Precio del producto")
ventana.geometry("600x300")

etiqueta_nombre=tk.Label(ventana, text="Ingrese el nombre: ").pack()
entrada_nombre=tk.Entry(ventana)
entrada_nombre.pack()

etiqueta_precio=tk.Label(ventana, text="Ingrese el precio: ").pack()
entrada_precio=tk.Entry(ventana)
entrada_precio.pack()

etiqueta_cantidad=tk.Label(ventana, text="Ingrese la cantidad del producto: ").pack()
entrada_cantidad=tk.Entry(ventana)
entrada_cantidad.pack()

envio_var=tk.BooleanVar()
garantia_var=tk.BooleanVar()
instalacion_var=tk.BooleanVar()
tk.Checkbutton(ventana, text="Envio a domicilio ($5.000)", variable=envio_var).pack()
tk.Checkbutton(ventana, text="Garantia extendida ($10.000)", variable=garantia_var).pack()
tk.Checkbutton(ventana, text="Instalacion ($15.000)", variable=instalacion_var).pack()


resultado = tk.Label(ventana, text="")
resultado.pack()

def calc():
    try:
        precio = float(entrada_precio.get())
        cantidad = int(entrada_cantidad.get())
    except ValueError:
        messagebox.showerror("Error.", "Complete el nombre y use valores positivos.")
        return

    subtotal = precio * cantidad

    servicio = 0
    if envio_var.get():
        servicio += 5000
    if garantia_var.get():
        servicio += 10000
    if instalacion_var.get():
        servicio += 15000

    total = subtotal + servicio

    if total >= 200000:
        descuento = total * 0.10
        total_final = total - descuento
        resultado.config(
            text=f"El total es: ${total_final:,.0f} (descuento aplicado: ${descuento:,.0f})"
        )
    else:
        resultado.config(text=f"El total es: ${total:,.0f}")

boton=tk.Button(ventana, text="Calcular", command=calc).pack()

boton_s=tk.Button(ventana, text="Salir", command=ventana.destroy).pack()

ventana.mainloop()