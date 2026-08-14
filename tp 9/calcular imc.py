import tkinter as tk

ventana = tk.Tk()
ventana.title("Calculador de IMC")
ventana.geometry("450x350")


def calcular_imc():
    try:
        peso = float(entrada_peso.get())
        altura = float(entrada_altura.get())

        if altura <= 0:
            raise ValueError

        imc = peso / (altura ** 2)

        if imc < 18.5:
            categoria = "Bajo peso"
        elif imc < 25:
            categoria = "Peso normal"
        elif imc < 30:
            categoria = "Sobrepeso"
        else:
            categoria = "Obesidad"

        etiqueta_imc.config(text=f"IMC: {imc:.2f}")
        etiqueta_categoria.config(text=f"Categoría: {categoria}")

    except ValueError:
        etiqueta_imc.config(text="Ingrese valores válidos")
        etiqueta_categoria.config(text="Peso y altura")


titulo = tk.Label(ventana, text="Calculadora de IMC")
titulo.pack()

etiqueta_peso = tk.Label(ventana, text="Peso (kg):")
etiqueta_peso.pack()
entrada_peso = tk.Entry(ventana)
entrada_peso.pack()

etiqueta_altura = tk.Label(ventana, text="Altura (m):")
etiqueta_altura.pack()
entrada_altura = tk.Entry(ventana)
entrada_altura.pack()

boton_calcular = tk.Button(ventana, text="Calcular", command=calcular_imc)
boton_calcular.pack()

etiqueta_imc = tk.Label(ventana, text="IMC:")
etiqueta_imc.pack()

etiqueta_categoria = tk.Label(ventana, text="Categoría")
etiqueta_categoria.pack()

ventana.mainloop()