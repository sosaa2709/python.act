import json  # Permite leer y guardar los datos en formato JSON.
from pathlib import Path  # Facilita crear y manejar rutas de archivos.
import ttkbootstrap as ttk  # Importa ttkbootstrap con el alias corto ttk.
from ttkbootstrap.constants import *  # Importa constantes de diseño como LEFT, X y SUCCESS.
from tkinter import messagebox  # Importa ventanas emergentes de aviso, error y confirmación.

ARCHIVO = Path(__file__).with_name("alumnos_crud.json")  # Usa un JSON propio junto a este programa.
alumnos = []  # Crea la lista que mantendrá los registros en memoria.
proximo_id = 1  # Define el primer identificador disponible para un alumno.


def cargar_datos():  # Lee del JSON los alumnos guardados anteriormente.
	global alumnos, proximo_id  # Indica que se actualizarán las variables globales.
	if not ARCHIVO.exists():  # Comprueba si el archivo todavía no fue creado.
		alumnos = []  # Empieza con una lista vacía si no existe el archivo.
		proximo_id = 1  # Reinicia el identificador al valor inicial.
		return  # Termina la función porque no hay datos para leer.

	try:  # Inicia el manejo de posibles errores al leer el JSON.
		with open(ARCHIVO, "r", encoding="utf-8") as archivo:  # Abre el archivo en modo lectura.
			alumnos = json.load(archivo)  # Convierte el contenido JSON en datos de Python.
		if alumnos:  # Comprueba si el archivo contiene al menos un alumno.
			proximo_id = max(alumno["id"] for alumno in alumnos) + 1  # Calcula el siguiente ID libre.
		else:  # Se ejecuta cuando el JSON contiene una lista vacía.
			proximo_id = 1  # Vuelve a usar el ID inicial.
	except (json.JSONDecodeError, OSError, KeyError, TypeError):  # Captura errores de lectura o estructura.
		messagebox.showerror("Error", "No se pudo cargar el archivo JSON.")  # Muestra el problema en una ventana.
		alumnos = []  # Deja la lista vacía para evitar datos incompletos.
		proximo_id = 1  # Reinicia el contador después del error.


def guardar_datos():  # Guarda la lista actual de alumnos en el archivo JSON.
	try:  # Inicia el manejo de posibles errores al escribir el archivo.
		with open(ARCHIVO, "w", encoding="utf-8") as archivo:  # Abre el archivo para escribirlo.
			json.dump(alumnos, archivo, indent=4, ensure_ascii=False)  # Escribe el JSON legible y conserva acentos.
		return True  # Indica que el guardado terminó correctamente.
	except OSError as error:  # Captura errores del sistema al guardar.
		messagebox.showerror("Error", f"No se pudieron guardar los datos.\n{error}")  # Muestra el detalle del error.
		return False  # Indica que el guardado falló.


def cargar_tabla(registros=None):  # Actualiza la tabla con todos los alumnos o con un filtro.
	for item in tabla.get_children():  # Recorre las filas que ya aparecen en la tabla.
		tabla.delete(item)  # Elimina cada fila anterior para evitar duplicados visuales.
	datos = alumnos if registros is None else registros  # Elige la lista completa o la lista filtrada.
	for alumno in datos:  # Recorre los alumnos que se mostrarán.
		tabla.insert(  # Agrega una fila nueva a la tabla.
			"",  # Indica que la fila se agrega en el nivel principal.
			"end",  # Coloca la fila al final de la tabla.
			iid=str(alumno["id"]),  # Usa el ID como identificador único de la fila.
			values=(  # Define los valores que se mostrarán en las columnas.
				alumno["id"],  # Muestra el ID del alumno.
				alumno["nombre"],  # Muestra el nombre del alumno.
				alumno["apellido"],  # Muestra el apellido del alumno.
				alumno["curso"],  # Muestra el curso del alumno.
			),  # Cierra la lista de valores de la fila.
		)  # Termina la llamada que agrega la fila.


def limpiar_formulario():  # Borra los campos y quita la selección de la tabla.
	entry_nombre.delete(0, END)  # Borra todo el texto del campo de nombre.
	entry_apellido.delete(0, END)  # Borra todo el texto del campo de apellido.
	combo_curso.set("")  # Deja vacío el selector de curso.
	tabla.selection_remove(tabla.selection())  # Quita la selección actual de la tabla.
	entry_nombre.focus()  # Coloca el cursor en el campo de nombre.


def agregar():  # Valida los campos y agrega un alumno nuevo.
	global proximo_id  # Permite incrementar el contador global de identificadores.
	nombre = entry_nombre.get().strip()  # Obtiene el nombre y quita espacios de los extremos.
	apellido = entry_apellido.get().strip()  # Obtiene el apellido y quita espacios de los extremos.
	curso = combo_curso.get().strip()  # Obtiene el curso y quita espacios de los extremos.
	if not nombre or not apellido or not curso:  # Comprueba que ningún campo esté vacío.
		messagebox.showwarning("Validación", "Complete todos los campos.")  # Pide completar la información.
		return  # Detiene el alta mientras falten datos.

	alumno = {  # Crea el registro del alumno como un diccionario.
		"id": proximo_id,  # Asigna el identificador actual.
		"nombre": nombre,  # Guarda el nombre ingresado.
		"apellido": apellido,  # Guarda el apellido ingresado.
		"curso": curso,  # Guarda el curso seleccionado.
	}  # Termina la creación del diccionario.
	alumnos.append(alumno)  # Añade el nuevo registro a la lista en memoria.
	if guardar_datos():  # Continúa solo si el archivo se guardó correctamente.
		proximo_id += 1  # Reserva el siguiente identificador.
		cargar_tabla()  # Actualiza la tabla para mostrar el alumno nuevo.
		limpiar_formulario()  # Limpia los campos después del alta.
		messagebox.showinfo("Alta", "Alumno agregado correctamente.")  # Confirma que se agregó.


def obtener_id_seleccionado():  # Devuelve el ID del alumno seleccionado en la tabla.
	seleccion = tabla.selection()  # Obtiene el identificador de la fila seleccionada.
	if not seleccion:  # Comprueba si no hay ninguna fila seleccionada.
		return None  # Informa que no hay ID seleccionado.
	return int(seleccion[0])  # Convierte y devuelve el identificador como número entero.


def cargar_seleccion(event):  # Copia al formulario los datos de la fila seleccionada.
	seleccion = event.widget.selection()  # Obtiene la selección desde la tabla que generó el evento.
	if not seleccion:  # Comprueba si el evento ocurrió sin una fila seleccionada.
		return  # Termina sin modificar el formulario.
	id_alumno = int(seleccion[0])  # Convierte el identificador seleccionado a entero.
	for alumno in alumnos:  # Busca el registro correspondiente dentro de la lista.
		if alumno["id"] == id_alumno:  # Comprueba si este registro es el seleccionado.
			entry_nombre.delete(0, END)  # Borra el contenido anterior del campo de nombre.
			entry_nombre.insert(0, alumno["nombre"])  # Coloca el nombre del alumno en el formulario.
			entry_apellido.delete(0, END)  # Borra el contenido anterior del campo de apellido.
			entry_apellido.insert(0, alumno["apellido"])  # Coloca el apellido del alumno en el formulario.
			combo_curso.set(alumno["curso"])  # Selecciona el curso que tiene guardado el alumno.
			break  # Termina la búsqueda porque ya se encontró el alumno.


def modificar():  # Actualiza los datos del alumno que está seleccionado.
	id_alumno = obtener_id_seleccionado()  # Obtiene el ID de la fila seleccionada.
	if id_alumno is None:  # Comprueba si el usuario no seleccionó un alumno.
		messagebox.showwarning("Modificar", "Seleccione un alumno.")  # Solicita seleccionar una fila.
		return  # Detiene la modificación.

	nombre = entry_nombre.get().strip()  # Lee el nombre editado y quita espacios externos.
	apellido = entry_apellido.get().strip()  # Lee el apellido editado y quita espacios externos.
	curso = combo_curso.get().strip()  # Lee el curso editado y quita espacios externos.
	if not nombre or not apellido or not curso:  # Comprueba que todos los campos estén completos.
		messagebox.showwarning("Validación", "Complete todos los campos.")  # Informa que falta algún dato.
		return  # Detiene la modificación hasta completar el formulario.

	for alumno in alumnos:  # Recorre los registros para encontrar el seleccionado.
		if alumno["id"] == id_alumno:  # Comprueba si encontró el ID buscado.
			alumno["nombre"] = nombre  # Reemplaza el nombre guardado.
			alumno["apellido"] = apellido  # Reemplaza el apellido guardado.
			alumno["curso"] = curso  # Reemplaza el curso guardado.
			break  # Termina el recorrido porque el alumno ya fue actualizado.

	if guardar_datos():  # Guarda los cambios y continúa si la escritura fue correcta.
		cargar_tabla()  # Refresca la tabla con los datos actualizados.
		limpiar_formulario()  # Limpia los campos y quita la selección.
		messagebox.showinfo("Modificar", "Alumno modificado correctamente.")  # Confirma la modificación.


def eliminar():  # Elimina el alumno seleccionado después de pedir confirmación.
	id_alumno = obtener_id_seleccionado()  # Obtiene el ID de la fila seleccionada.
	if id_alumno is None:  # Comprueba si no se seleccionó ningún alumno.
		messagebox.showwarning("Eliminar", "Seleccione un alumno.")  # Solicita seleccionar una fila.
		return  # Detiene la eliminación.

	confirmar = messagebox.askyesno(  # Abre un cuadro para confirmar la eliminación.
		"Confirmar",  # Define el título del cuadro de confirmación.
		"¿Desea eliminar el alumno seleccionado?",  # Define la pregunta que se muestra.
	)  # Termina la llamada al cuadro de confirmación.
	if not confirmar:  # Comprueba si el usuario eligió No.
		return  # Cancela la eliminación.

	for alumno in alumnos:  # Recorre la lista para encontrar el alumno seleccionado.
		if alumno["id"] == id_alumno:  # Comprueba si el ID coincide.
			alumnos.remove(alumno)  # Quita el alumno de la lista en memoria.
			break  # Termina el recorrido porque ya se eliminó el alumno.

	if guardar_datos():  # Persiste la lista actualizada en el archivo JSON.
		cargar_tabla()  # Refresca la tabla sin el alumno eliminado.
		limpiar_formulario()  # Limpia los campos del formulario.
		messagebox.showinfo("Eliminar", "Alumno eliminado correctamente.")  # Confirma la eliminación.


def buscar():  # Filtra alumnos según el texto ingresado en el campo de búsqueda.
	texto = entry_busqueda.get().strip().lower()  # Lee el texto y lo normaliza a minúsculas.
	if not texto:  # Comprueba si el campo de búsqueda está vacío.
		cargar_tabla()  # Muestra todos los alumnos si no hay texto para buscar.
		return  # Termina porque no hace falta aplicar un filtro.

	filtrados = [  # Construye una lista con los alumnos que coinciden con la búsqueda.
		alumno  # Incluye este alumno en el resultado si cumple las condiciones.
		for alumno in alumnos  # Revisa cada alumno guardado.
		if texto in alumno["nombre"].lower()  # Busca el texto dentro del nombre.
		or texto in alumno["apellido"].lower()  # También busca dentro del apellido.
		or texto in alumno["curso"].lower()  # También busca dentro del curso.
	]  # Termina la comprensión de lista.
	cargar_tabla(filtrados)  # Muestra en la tabla solo los resultados encontrados.


# ---------------- INTERFAZ ----------------  # Separa visualmente la lógica de la creación de la ventana.
app = ttk.Window(themename="flatly")  # Crea la ventana principal con el tema flatly.
app.title("Gestión de Alumnos - JSON")  # Define el título que aparece en la ventana.
app.geometry("850x600")  # Establece el tamaño inicial de la ventana.
app.minsize(750, 500)  # Evita que la ventana se reduzca por debajo de este tamaño.
cargar_datos()  # Carga del JSON los alumnos guardados al iniciar.
contenedor = ttk.Frame(app, padding=15)  # Crea el marco principal con espacio interno.
contenedor.pack(fill=BOTH, expand=True)  # Expande el marco para ocupar la ventana.
formulario = ttk.LabelFrame(contenedor, text="Datos del alumno", padding=15)  # Crea el grupo visual del formulario.
formulario.pack(fill=X, pady=(0, 10))  # Expande el formulario horizontalmente y agrega margen inferior.
formulario.columnconfigure(1, weight=1)  # Permite que la columna del nombre se estire.
formulario.columnconfigure(3, weight=1)  # Permite que la columna del apellido se estire.
ttk.Label(formulario, text="Nombre:").grid(  # Crea y ubica la etiqueta del nombre.
	row=0, column=0, padx=5, pady=5, sticky=W  # La pone en la primera fila y la alinea a la izquierda.
)  # Termina la configuración de la etiqueta del nombre.
entry_nombre = ttk.Entry(formulario)  # Crea el campo para escribir el nombre.
entry_nombre.grid(row=0, column=1, padx=5, pady=5, sticky=EW)  # Ubica y estira el campo del nombre.
ttk.Label(formulario, text="Apellido:").grid(  # Crea y ubica la etiqueta del apellido.
	row=0, column=2, padx=5, pady=5, sticky=W  # La pone en la primera fila, a la derecha del nombre.
)  # Termina la configuración de la etiqueta del apellido.
entry_apellido = ttk.Entry(formulario)  # Crea el campo para escribir el apellido.
entry_apellido.grid(row=0, column=3, padx=5, pady=5, sticky=EW)  # Ubica y estira el campo del apellido.
ttk.Label(formulario, text="Curso:").grid(  # Crea y ubica la etiqueta del curso.
	row=1, column=0, padx=5, pady=5, sticky=W  # La pone en la segunda fila, alineada a la izquierda.
)  # Termina la configuración de la etiqueta del curso.
combo_curso = ttk.Combobox(  # Crea una lista desplegable para elegir el curso.
	formulario,  # Indica que el selector pertenece al formulario.
	values=["1°A", "1°B", "2°A", "2°B", "3°A", "3°B"],  # Define las opciones disponibles.
	state="readonly",  # Impide escribir valores que no estén en la lista.
)  # Termina la creación del selector de curso.
combo_curso.grid(row=1, column=1, padx=5, pady=5, sticky=EW)  # Ubica y estira el selector de curso.
botones = ttk.Frame(contenedor)  # Crea un marco para agrupar los botones de acciones.
botones.pack(fill=X, pady=5)  # Expande el marco de botones y agrega margen vertical.
ttk.Button(botones, text="Agregar", bootstyle=SUCCESS, command=agregar).pack(  # Crea el botón para dar de alta.
	side=LEFT, padx=4  # Lo coloca a la izquierda y agrega espacio lateral.
)  # Termina la creación y ubicación del botón Agregar.
ttk.Button(botones, text="Modificar", bootstyle=WARNING, command=modificar).pack(  # Crea el botón para editar.
	side=LEFT, padx=4  # Lo coloca junto a los demás botones con margen lateral.
)  # Termina la creación y ubicación del botón Modificar.
ttk.Button(botones, text="Eliminar", bootstyle=DANGER, command=eliminar).pack(  # Crea el botón para borrar.
	side=LEFT, padx=4  # Lo coloca junto a los demás botones con margen lateral.
)  # Termina la creación y ubicación del botón Eliminar.
ttk.Button(  # Empieza la configuración del botón para limpiar el formulario.
	botones,  # Indica que el botón pertenece al marco de acciones.
	text="Limpiar",  # Define el texto que verá el usuario.
	bootstyle=SECONDARY,  # Aplica el estilo secundario del tema.
	command=limpiar_formulario,  # Ejecuta la función que borra los campos al hacer clic.
).pack(side=LEFT, padx=4)  # Coloca el botón a la izquierda con margen lateral.
busqueda = ttk.Frame(contenedor)  # Crea un marco independiente para la búsqueda.
busqueda.pack(fill=X, pady=10)  # Expande el marco y agrega espacio vertical.
ttk.Label(busqueda, text="Buscar:").pack(side=LEFT, padx=5)  # Muestra la etiqueta a la izquierda del campo.
entry_busqueda = ttk.Entry(busqueda)  # Crea el campo donde se escribe el texto a buscar.
entry_busqueda.pack(side=LEFT, fill=X, expand=True, padx=5)  # Ubica el campo y permite que se estire.
ttk.Button(busqueda, text="Buscar", bootstyle=INFO, command=buscar).pack(side=LEFT, padx=5)  # Crea el botón que aplica el filtro.
ttk.Button(  # Empieza la configuración del botón para quitar el filtro.
	busqueda,  # Indica que el botón pertenece al marco de búsqueda.
	text="Mostrar todos",  # Define el texto del botón.
	command=lambda: cargar_tabla(),  # Muestra todos los alumnos al hacer clic.
).pack(side=LEFT, padx=5)  # Coloca el botón al lado del campo de búsqueda.
tabla = ttk.Treeview(  # Crea la tabla donde se mostrarán los alumnos.
	contenedor,  # Indica que la tabla pertenece al contenedor principal.
	columns=("id", "nombre", "apellido", "curso"),  # Define las cuatro columnas de datos.
	show="headings",  # Muestra encabezados en lugar de una columna de árbol.
	selectmode="browse",  # Permite seleccionar una sola fila por vez.
)  # Termina la creación de la tabla.
tabla.heading("id", text="ID")  # Define el encabezado de la columna ID.
tabla.heading("nombre", text="Nombre")  # Define el encabezado de la columna Nombre.
tabla.heading("apellido", text="Apellido")  # Define el encabezado de la columna Apellido.
tabla.heading("curso", text="Curso")  # Define el encabezado de la columna Curso.
tabla.column("id", width=60, anchor=CENTER)  # Ajusta el ancho y centra los ID.
tabla.column("nombre", width=180)  # Define el ancho de la columna Nombre.
tabla.column("apellido", width=180)  # Define el ancho de la columna Apellido.
tabla.column("curso", width=100, anchor=CENTER)  # Ajusta el ancho y centra el curso.
tabla.pack(fill=BOTH, expand=True)  # Expande la tabla para ocupar el espacio disponible.
tabla.bind("<<TreeviewSelect>>", cargar_seleccion)  # Carga los datos en el formulario al seleccionar una fila.
cargar_tabla()  # Muestra en la tabla los datos que se cargaron del JSON.
entry_nombre.focus()  # Deja el cursor listo en el campo de nombre.
app.mainloop()  # Inicia el ciclo de eventos y mantiene abierta la aplicación.