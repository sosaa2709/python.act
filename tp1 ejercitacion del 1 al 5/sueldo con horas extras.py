import tkinter as tk 
ventana=tk.Tk()
ventana.title("calculadora de sueldos")
ventana.geometry("450x300")

etiqueta_nombre=tk.Label(ventana, text="Ingrese nombre: ")
etiqueta_nombre.pack()
entrada_nombre=tk.Entry(ventana)
entrada_nombre.pack()

etiqueta_sueldo=tk.Label(ventana, text="Ingrese sueldo basico: ")
etiqueta_sueldo.pack()
entrada_sueldo=tk.Entry(ventana)
entrada_sueldo.pack()

etiqueta_horas=tk.Label(ventana, text="Ingrese horas extras: ")
etiqueta_horas.pack()
entrada_horas=tk.Entry(ventana)
entrada_horas.pack()

def sueldo_final():
    sueldo = float(entrada_sueldo.get())
    horas = int(entrada_horas.get())
    sueldo_fin = sueldo + horas * 5000
    if sueldo_fin < 500000:
        tipo_sueldo = "Sueldo bajo"
    elif sueldo_fin <= 1000000:
        tipo_sueldo = "Sueldo medio"
    else:
        tipo_sueldo = "Sueldo alto"

    etiqueta_resultado.config(
        text=f"Sueldo final: ${sueldo_fin}\nClasificación: {tipo_sueldo}"
    )

boton=tk.Button(ventana, text="Mostrar ", command=sueldo_final)
boton.pack()

etiqueta_resultado=tk.Label(ventana, text="")
etiqueta_resultado.pack()

boton_s=tk.Button(ventana, text="Salir", command=ventana.destroy)
boton_s.pack()

ventana.mainloop()
