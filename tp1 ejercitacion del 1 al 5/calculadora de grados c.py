import tkinter as tk 
ventana=tk.Tk()
ventana.title("Calculadora de grados C")
ventana.geometry("450x350")

def gradosc_gradosf():
    celsius=int(entrada_celsius.get())
    fahrenheit=(celsius * (9/5)) + 32
    etiqueta_resultado.config(text=f"Fahrenheit: {fahrenheit}")

etiqueta_celsius = tk.Label(ventana, text="Celcius:")
etiqueta_celsius.pack()
entrada_celsius = tk.Entry(ventana)
entrada_celsius.pack()

boton_calcular = tk.Button(ventana, text="Calcular", command=gradosc_gradosf)
boton_calcular.pack()

etiqueta_resultado=tk.Label(ventana, text="Fahrenheit")
etiqueta_resultado.pack()

ventana.mainloop()