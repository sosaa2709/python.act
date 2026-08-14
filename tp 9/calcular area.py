import tkinter as tk 
ventana=tk.Tk()
ventana.title("Calcular area")
ventana.geometry("420x250")

def calc_area():
    base=int(entrada_base.get())
    altura=int(entrada_altura.get())
    area =base*altura
    etiqueta_resultado.config(text=f"Area: {area}")

etiqueta_base=tk.Label(
    ventana,
    text="Base"
)
etiqueta_base.pack()
entrada_base=tk.Entry(ventana)
entrada_base.pack()

etiqueta_altura=tk.Label(
    ventana, 
    text="Altura"
)
etiqueta_altura.pack()
entrada_altura=tk.Entry(ventana)
entrada_altura.pack()

etiqueta_resultado=tk.Label(
    ventana,
    text="Area: "
)
etiqueta_resultado.pack()

boton=tk.Button(
    ventana,
    text="Calcular area: ",
    command=calc_area
)
boton.pack()

ventana.mainloop()