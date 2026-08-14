import tkinter as tk

ventana = tk.Tk()

ventana.title ("Mi primera ventana")
ventana.geometry ("400x250")

etiqueta = tk.Label(
    ventana,
    text="Bienvenido a python"
)

etiqueta.pack()

boton=tk.Button(
    ventana,
    text="Salir",
    command=ventana.destroy,
    bg="pink",
    fg="red",
    borderwidth=5
)

boton.pack()

ventana.mainloop()