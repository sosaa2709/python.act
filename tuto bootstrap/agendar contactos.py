import tkinter as tk  # Importa la librería Tkinter para crear interfaces gráficas
from tkinter import ttk  # Importa los widgets modernos de Tkinter (ttk)
ventana = tk.Tk()  # Crea la ventana principal de la aplicación
ventana.title("contactos")  # Coloca el título "contactos" en la ventana principal
ventana.geometry("650x400")  # Define el tamaño inicial de la ventana: 1920x1080 px


def apert():  # Define la función que abre la ventana para agregar contactos
    ventana_num = tk.Toplevel(ventana)  # Crea una ventana secundaria dentro de la ventana principal
    ventana_num.title("agregar contacto")  # Pone el título "agregar contacto" en la ventana secundaria
    ventana_num.geometry("400x250")  # Establece el tamaño de la ventana secundaria: 400x250 px

    nombre_etiqueta = ttk.Label(  # Crea una etiqueta para mostrar "nombre"
        ventana_num,  # La etiqueta se coloca en la ventana secundaria
        text="nombre"  # Texto que se muestra en la etiqueta
    ).pack()  # Muestra la etiqueta en pantalla

    nombre_entry = ttk.Entry(ventana_num)  # Crea un campo de texto para ingresar el nombre
    nombre_entry.pack()  # Muestra el campo de texto

    telefono_label = ttk.Label(  # Crea una etiqueta para mostrar "telèfono"
        ventana_num,  # La etiqueta va dentro de la ventana secundaria
        text="telèfono"  # Texto de la etiqueta
    ).pack()  # Muestra la etiqueta

    telefono_entry = ttk.Entry(ventana_num)  # Crea un campo para ingresar el teléfono
    telefono_entry.pack()  # Muestra el campo de texto

    correo_label = ttk.Label(  # Crea una etiqueta para mostrar "correo electronico"
        ventana_num,  # La etiqueta se coloca en la ventana secundaria
        text="correo electronico"  # Texto de la etiqueta
    ).pack()  # Muestra la etiqueta

    correo_entry = ttk.Entry(ventana_num)  # Crea un campo para ingresar el correo
    correo_entry.pack()  # Muestra el campo de texto

    def contactis():  # Define una función interna para guardar el contacto en la lista
        nombre = nombre_entry.get()  # Obtiene el texto ingresado en el campo de nombre
        telefono = telefono_entry.get()  # Obtiene el texto ingresado en el campo de teléfono
        correo = correo_entry.get()  # Obtiene el texto ingresado en el campo de correo
        contacto = f"{nombre} // {telefono} // {correo}"  # Crea un texto con los datos del contacto
        contactos.insert(tk.END, contacto)  # Agrega ese contacto al final de la lista visible

    def botonardo():  # Define la función que se ejecuta cuando se presiona el botón ingresar
        contactis()  # Llama a la función que guarda el contacto
        ventana_num.destroy()  # Cierra la ventana secundaria

    agregar_bot = ttk.Button(  # Crea el botón para guardar el contacto
        ventana_num,  # El botón se coloca en la ventana secundaria
        text="ingresar",  # Texto que muestra el botón
        command=botonardo  # Al hacer clic ejecuta la función botonardo
    )
    agregar_bot.pack()  # Muestra el botón en la ventana


def borrar_contacto():  # Define la función para borrar un contacto seleccionado
    seleccionado = contactos.curselection()  # Obtiene la posición del contacto seleccionado en la lista
    if seleccionado:  # Si hay algo seleccionado, ejecuta el bloque
        contactos.delete(seleccionado[0])  # Elimina el contacto de la lista en la posición seleccionada


cont = ttk.Label(  # Crea una etiqueta con el texto "contactos"
    ventana,  # La etiqueta se coloca en la ventana principal
    text="contactos"  # Texto de la etiqueta
).pack()  # Muestra la etiqueta

contactos = tk.Listbox(ventana, width=60, height=10)  # Crea la lista de contactos en la ventana principal
contactos.pack(padx=20, pady=20)  # Muestra la lista con márgenes alrededor


apret_bot = ttk.Button(  # Crea el botón de "agregar contacto"
    ventana,  # Lo coloca en la ventana principal
    text="agregar contacto",  # Texto del botón
    command=apert  # Cuando se haga clic, abre la ventana para agregar contactos
)

borrar_bot = tk.Button(  # Crea el botón para borrar contacto
    ventana,  # Lo coloca en la ventana principal
    text="borrar contacto",  # Texto del botón
    command=borrar_contacto  # Ejecuta la función para borrar el contacto seleccionado
)

apret_bot.pack()  # Muestra el botón de agregar contacto
borrar_bot.pack()  # Muestra el botón de borrar contacto

boton = tk.Button(  # Crea el botón de salir
    ventana,  # Lo coloca en la ventana principal
    text="salir",  # Texto del botón
    command=ventana.destroy  # Al hacer clic, cierra la ventana principal
)
boton.pack()  # Muestra el botón de salir


ventana.mainloop()  # Inicia el ciclo principal de la aplicación para mantenerla abierta y funcionando