import tkinter as tk 
ventana=tk.Tk()
ventana.title("positivo o negativo")
ventana.geometry("450x300")

etiqueta_numero=tk.Label(ventana, text="Ingrese el numero ")
etiqueta_numero.pack()
entrada_numero=tk.Entry(ventana)
entrada_numero.pack()

def pos_neg():
    numero=int(entrada_numero.get())
    if numero > 0: 
        etiqueta_resultado.config(text="Positivo")
    elif numero < 0:
        etiqueta_resultado.config(text="Negativo")
    else:
        etiqueta_resultado.config(text="No puede ser 0")

boton=tk.Button(ventana, text="Mostrar", command=pos_neg)
boton.pack()

etiqueta_resultado=tk.Label(ventana, text="")
etiqueta_resultado.pack()

boton_s=tk.Button(ventana, text="Salir", command=ventana.destroy)
boton_s.pack(pady=10)

ventana.mainloop()