import tkinter as tk
ventana=tk.Tk()

ventana.title("Calculadora")
ventana.geometry("400x250")

def sumar():
    numero1=int(entrada1.get())
    numero2=int(entrada2.get())

    resultado=numero1+numero2
    etiqueta_resultado.config(
        text="Resultado: " + str(resultado)
    )

etiqueta1=tk.Label(
    ventana,
    text="Numero 1:"
)
etiqueta1.pack()
entrada1=tk.Entry(ventana)
entrada1.pack()

etiqueta2=tk.Label(
    ventana,
    text="Numero 2:"
)
etiqueta2.pack()
entrada2=tk.Entry(ventana)
entrada2.pack()

boton_sumar=tk.Button(
    ventana,
    text="Sumar",
    command=sumar
)
boton_sumar.pack()

etiqueta_resultado=tk.Label(
    ventana,
    text="Resultado:"
)
etiqueta_resultado.pack()

ventana.mainloop()