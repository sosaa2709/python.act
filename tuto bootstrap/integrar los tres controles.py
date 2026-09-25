import ttkbootstrap as ttk 
ventana=ttk.Window(themename="darkly")
ventana.title("Holis")
ventana.geometry("500x300")
ventana.configure(bg="#0a0a0a")

ttk.Label(ventana, text="Nombre: ").pack(pady=10)
ttk.Entry(ventana).pack(pady=10)
ttk.Button(ventana, text="Aceptar").pack(pady=10)

ventana.mainloop()