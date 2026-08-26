import tkinter as tk 
ventana=tk.Tk()
ventana.title("calculadora de sueldos")
ventana.geometry("450x300")

etiqueta_nombre=tk.Label(ventana, text="Ingrese el nombre del producto: ")
etiqueta_nombre.pack()
entrada_nombre=tk.Entry(ventana)
entrada_nombre.pack()

etiqueta_precio=tk.Label(ventana, text="Ingrese el precio del producto: ")
etiqueta_precio.pack()
entrada_precio=tk.Entry(ventana)
entrada_precio.pack()

etiqueta_porcen=tk.Label(ventana, text="Ingrese el porcentaje del descuento: ")
etiqueta_porcen.pack()
entrada_porcen=tk.Entry(ventana)
entrada_porcen.pack()

def descuento_producto():
    precio=int(entrada_precio.get())
    porcen=int(entrada_porcen.get())
    descuento=(precio*porcen)/100
    precio_final=precio - descuento
    etiqueta_resultado.config(text=f"Precio final: {precio_final}")

boton=tk.Button(ventana, text="Mostrar", command=descuento_producto)
boton.pack()

etiqueta_resultado=tk.Label(ventana, text="")
etiqueta_resultado.pack()

boton_s=tk.Button(ventana, text="Salir", command=ventana.destroy)
boton_s.pack()

ventana.mainloop()
