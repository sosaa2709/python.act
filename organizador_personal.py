import csv
import json
import os
import tkinter as tk
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Dict, List, Optional
import ttkbootstrap as ttk


DATA_FILE = Path(__file__).with_name("organizador_datos.json")
PRIORITIES = ("Alta", "Media", "Baja")
PRIORITY_ORDER = {"Alta": 0, "Media": 1, "Baja": 2}


@dataclass
class Task:
    id: str
    title: str
    description: str
    due_date: str
    priority: str
    completed: bool
    created_at: str

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        if not isinstance(data, dict):
            raise ValueError("Cada tarea debe ser un objeto JSON.")

        task_id = data.get("id")
        title = data.get("title")
        description = data.get("description", "")
        due_date = data.get("due_date", "")
        priority = data.get("priority", "Media")
        completed = data.get("completed", False)
        created_at = data.get("created_at", datetime.now().isoformat(timespec="seconds"))

        if not isinstance(task_id, str) or not task_id:
            raise ValueError("Hay una tarea sin identificador valido.")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Hay una tarea sin titulo valido.")
        if not isinstance(description, str) or not isinstance(due_date, str):
            raise ValueError("La descripcion y la fecha deben ser texto.")
        if priority not in PRIORITIES:
            raise ValueError("Una tarea tiene una prioridad desconocida.")
        if not isinstance(completed, bool) or not isinstance(created_at, str):
            raise ValueError("El estado o la fecha de creacion no son validos.")
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError as error:
                raise ValueError("Una tarea tiene una fecha limite invalida.") from error

        return cls(task_id, title, description, due_date, priority, completed, created_at)


class TaskStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.tasks = self._load()

    def _load(self) -> List[Task]:
        if not self.path.exists():
            return []
        try:
            with self.path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError) as error:
            raise ValueError("No se pudo leer el archivo de tareas.") from error
        if not isinstance(data, list):
            raise ValueError("El archivo de tareas debe contener una lista.")
        return [Task.from_dict(item) for item in data]

    def _save(self, tasks: List[Task]) -> None:
        temporary_path = self.path.with_name(self.path.name + ".tmp")
        try:
            with temporary_path.open("w", encoding="utf-8") as file:
                json.dump([asdict(task) for task in tasks], file, indent=2, ensure_ascii=False)
            os.replace(temporary_path, self.path)
        except OSError:
            try:
                temporary_path.unlink()
            except OSError:
                pass
            raise

    def _commit(self, tasks: List[Task]) -> None:
        self._save(tasks)
        self.tasks = tasks

    def add(self, title: str, description: str, due_date: str, priority: str) -> Task:
        task = Task(
            id=datetime.now().strftime("%Y%m%d%H%M%S%f"),
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            completed=False,
            created_at=datetime.now().isoformat(timespec="seconds"),
        )
        self._commit(self.tasks + [task])
        return task

    def update(self, task_id: str, values: Dict[str, str]) -> None:
        if not any(task.id == task_id for task in self.tasks):
            raise KeyError("No se encontro la tarea seleccionada.")
        updated = [
            Task(
                id=task.id,
                title=values["title"],
                description=values["description"],
                due_date=values["due_date"],
                priority=values["priority"],
                completed=task.completed,
                created_at=task.created_at,
            )
            if task.id == task_id
            else task
            for task in self.tasks
        ]
        self._commit(updated)

    def toggle(self, task_id: str) -> None:
        updated = [
            Task(**{**asdict(task), "completed": not task.completed})
            if task.id == task_id
            else task
            for task in self.tasks
        ]
        if updated == self.tasks:
            raise KeyError("No se encontro la tarea seleccionada.")
        self._commit(updated)

    def delete(self, task_id: str) -> None:
        updated = [task for task in self.tasks if task.id != task_id]
        if len(updated) == len(self.tasks):
            raise KeyError("No se encontro la tarea seleccionada.")
        self._commit(updated)


class TaskDialog(tk.Toplevel):
    def __init__(self, parent: tk.Tk, task: Optional[Task] = None) -> None:
        super().__init__(parent)
        self.result: Optional[Dict[str, str]] = None
        self.title("Editar tarea" if task else "Nueva tarea")
        self.transient(parent)
        self.resizable(False, False)
        self.configure(padx=20, pady=18)
        self.columnconfigure(1, weight=1)

        self.title_var = tk.StringVar(value=task.title if task else "")
        self.date_var = tk.StringVar(value=task.due_date if task else "")
        self.priority_var = tk.StringVar(value=task.priority if task else "Media")

        ttk.Label(self, text="Titulo").grid(row=0, column=0, sticky="w", padx=(0, 12), pady=6)
        title_entry = ttk.Entry(self, textvariable=self.title_var, width=42)
        title_entry.grid(row=0, column=1, sticky="ew", pady=6)

        ttk.Label(self, text="Fecha limite").grid(row=1, column=0, sticky="w", padx=(0, 12), pady=6)
        date_entry = ttk.Entry(self, textvariable=self.date_var)
        date_entry.grid(row=1, column=1, sticky="ew", pady=6)
        ttk.Label(self, text="Formato: AAAA-MM-DD; dejar vacio si no aplica", style="Hint.TLabel").grid(
            row=2, column=1, sticky="w", pady=(0, 6)
        )

        ttk.Label(self, text="Prioridad").grid(row=3, column=0, sticky="w", padx=(0, 12), pady=6)
        ttk.Combobox(
            self,
            textvariable=self.priority_var,
            values=PRIORITIES,
            state="readonly",
        ).grid(row=3, column=1, sticky="ew", pady=6)

        ttk.Label(self, text="Descripcion").grid(row=4, column=0, sticky="nw", padx=(0, 12), pady=6)
        self.description_text = tk.Text(self, width=42, height=6, wrap="word", undo=True)
        self.description_text.grid(row=4, column=1, sticky="ew", pady=6)
        if task:
            self.description_text.insert("1.0", task.description)

        buttons = ttk.Frame(self)
        buttons.grid(row=5, column=0, columnspan=2, sticky="e", pady=(14, 0))
        ttk.Button(buttons, text="Cancelar", command=self.destroy).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Guardar", bootstyle="success", command=self._save).pack(side="left")

        self.bind("<Escape>", lambda _event: self.destroy())
        self.grab_set()
        title_entry.focus_set()
        self.update_idletasks()
        self.geometry(f"+{parent.winfo_rootx() + 80}+{parent.winfo_rooty() + 60}")

    def _save(self) -> None:
        title = self.title_var.get().strip()
        due_date = self.date_var.get().strip()
        if not title:
            messagebox.showwarning("Falta el titulo", "Escribe un titulo para la tarea.", parent=self)
            return
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning(
                    "Fecha invalida",
                    "Usa el formato AAAA-MM-DD, por ejemplo 2026-10-30.",
                    parent=self,
                )
                return
        self.result = {
            "title": title,
            "description": self.description_text.get("1.0", "end-1c").strip(),
            "due_date": due_date,
            "priority": self.priority_var.get(),
        }
        self.destroy()


class OrganizerApp:
    def __init__(self, root: tk.Tk, store: TaskStore) -> None:
        self.root = root
        self.store = store
        self.search_var = tk.StringVar()
        self.status_filter = tk.StringVar(value="Todas")
        self.priority_filter = tk.StringVar(value="Todas")
        self.detail_var = tk.StringVar(value="Selecciona una tarea para ver su descripcion.")
        self.sort_column = "due_date"
        self.sort_descending = False
        self.stat_vars = {name: tk.StringVar(value="0") for name in ("Total", "Pendientes", "Completadas", "Vencidas")}

        self.root.title("Organizador personal")
        self.root.geometry("1080x760")
        self.root.minsize(820, 600)
        self._configure_style()
        self._build_ui()
        self.search_var.trace_add("write", lambda *_args: self.refresh())
        self.root.bind("<Control-n>", lambda _event: self.add_task())
        self.root.bind("<Control-e>", lambda _event: self.edit_task())
        self.root.bind("<Control-f>", lambda _event: self.search_entry.focus_set())
        self.refresh()

    def _configure_style(self) -> None:
        style = ttk.Style()
        self.root.configure(background="#f1f4f2")
        style.configure("TFrame", background="#f1f4f2")
        style.configure("Header.TFrame", background="#183b35")
        style.configure("HeaderTitle.TLabel", background="#183b35", foreground="#ffffff", font=("Segoe UI", 23, "bold"))
        style.configure("HeaderSub.TLabel", background="#183b35", foreground="#d7e5df", font=("Segoe UI", 10))
        style.configure("StatValue.TLabel", font=("Segoe UI", 19, "bold"), foreground="#183b35")
        style.configure("StatName.TLabel", foreground="#52645e", font=("Segoe UI", 9, "bold"))
        style.configure("Hint.TLabel", foreground="#64746e", font=("Segoe UI", 9))
        style.configure("Treeview", rowheight=32, font=("Segoe UI", 10), background="#ffffff", fieldbackground="#ffffff")
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), padding=(8, 8))
        style.map("Treeview", background=[("selected", "#b8d5c9")], foreground=[("selected", "#183b35")])

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=18)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(3, weight=1)

        header = ttk.Frame(container, style="Header.TFrame", padding=(22, 18))
        header.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        header.columnconfigure(0, weight=1)
        ttk.Label(header, text="Organizador personal", style="HeaderTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(header, text="Tareas claras, prioridades bajo control.", style="HeaderSub.TLabel").grid(
            row=1, column=0, sticky="w", pady=(3, 0)
        )
        ttk.Label(header, text=date.today().strftime("%d/%m/%Y"), style="HeaderSub.TLabel").grid(
            row=0, column=1, rowspan=2, sticky="e", padx=(18, 0)
        )

        stats = ttk.Frame(container, padding=(4, 4, 4, 12))
        stats.grid(row=1, column=0, sticky="ew")
        for index, name in enumerate(self.stat_vars):
            stats.columnconfigure(index, weight=1)
            cell = ttk.Frame(stats, padding=(12, 8))
            cell.grid(row=0, column=index, sticky="ew", padx=(0 if index == 0 else 6, 6))
            ttk.Label(cell, textvariable=self.stat_vars[name], style="StatValue.TLabel").pack(anchor="w")
            ttk.Label(cell, text=name.upper(), style="StatName.TLabel").pack(anchor="w", pady=(2, 0))

        toolbar = ttk.Frame(container)
        toolbar.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        toolbar.columnconfigure(1, weight=1)
        ttk.Label(toolbar, text="Buscar").grid(row=0, column=0, padx=(0, 8))
        self.search_entry = ttk.Entry(toolbar, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        ttk.Combobox(
            toolbar,
            textvariable=self.status_filter,
            values=("Todas", "Pendientes", "Completadas", "Vencidas"),
            state="readonly",
            width=14,
        ).grid(row=0, column=2, padx=(0, 8))
        ttk.Combobox(
            toolbar,
            textvariable=self.priority_filter,
            values=("Todas",) + PRIORITIES,
            state="readonly",
            width=11,
        ).grid(row=0, column=3, padx=(0, 10))
        ttk.Button(toolbar, text="+ Nueva tarea", bootstyle="success", command=self.add_task).grid(row=0, column=4)
        self.status_filter.trace_add("write", lambda *_args: self.refresh())
        self.priority_filter.trace_add("write", lambda *_args: self.refresh())

        list_frame = ttk.Frame(container)
        list_frame.grid(row=3, column=0, sticky="nsew")
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        columns = ("title", "priority", "due_date", "status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")
        headings = {"title": "Tarea", "priority": "Prioridad", "due_date": "Fecha limite", "status": "Estado"}
        widths = {"title": 430, "priority": 120, "due_date": 130, "status": 130}
        for column in columns:
            self.tree.heading(column, text=headings[column], command=lambda key=column: self._sort_by(key))
            self.tree.column(column, width=widths[column], anchor="w" if column == "title" else "center")
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.tag_configure("Alta", foreground="#a33b2f")
        self.tree.tag_configure("Media", foreground="#98651b")
        self.tree.tag_configure("Baja", foreground="#28704f")
        self.tree.tag_configure("Completada", foreground="#79847f")
        self.tree.tag_configure("Vencida", background="#fff0e8", foreground="#a33b2f")
        self.tree.bind("<<TreeviewSelect>>", self._show_details)
        self.tree.bind("<Double-1>", lambda _event: self.edit_task())
        self.tree.bind("<Delete>", lambda _event: self.delete_task())

        actions = ttk.Frame(container, padding=(0, 10, 0, 8))
        actions.grid(row=4, column=0, sticky="ew")
        ttk.Button(actions, text="Editar", bootstyle="secondary", command=self.edit_task).pack(side="left", padx=(0, 7))
        ttk.Button(actions, text="Completar / reabrir", bootstyle="success-outline", command=self.toggle_task).pack(side="left", padx=7)
        ttk.Button(actions, text="Eliminar", bootstyle="danger-outline", command=self.delete_task).pack(side="left", padx=7)
        ttk.Button(actions, text="Exportar CSV", bootstyle="info-outline", command=self.export_csv).pack(side="right")

        details = ttk.LabelFrame(container, text="Detalle", padding=(12, 8))
        details.grid(row=5, column=0, sticky="ew")
        ttk.Label(details, textvariable=self.detail_var, wraplength=950, justify="left").pack(anchor="w")
        self.status_var = tk.StringVar(value="Listo")
        ttk.Label(container, textvariable=self.status_var, style="Hint.TLabel").grid(
            row=6, column=0, sticky="w", pady=(7, 0)
        )

    def _visible_tasks(self) -> List[Task]:
        query = self.search_var.get().strip().casefold()
        status = self.status_filter.get()
        priority = self.priority_filter.get()
        today = date.today().isoformat()
        tasks = []
        for task in self.store.tasks:
            if query and query not in (task.title + " " + task.description).casefold():
                continue
            if status == "Pendientes" and task.completed:
                continue
            if status == "Completadas" and not task.completed:
                continue
            if status == "Vencidas" and (task.completed or not task.due_date or task.due_date >= today):
                continue
            if priority != "Todas" and task.priority != priority:
                continue
            tasks.append(task)

        key_functions = {
            "title": lambda task: task.title.casefold(),
            "priority": lambda task: PRIORITY_ORDER[task.priority],
            "due_date": lambda task: (not bool(task.due_date), task.due_date),
            "status": lambda task: task.completed,
        }
        return sorted(tasks, key=key_functions[self.sort_column], reverse=self.sort_descending)

    def refresh(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        today = date.today().isoformat()
        for task in self._visible_tasks():
            if task.completed:
                tag = "Completada"
                status = "Completada"
            elif task.due_date and task.due_date < today:
                tag = "Vencida"
                status = "Vencida"
            else:
                tag = task.priority
                status = "Pendiente"
            self.tree.insert(
                "",
                "end",
                iid=task.id,
                values=(task.title, task.priority, task.due_date or "Sin fecha", status),
                tags=(tag,),
            )

        all_tasks = self.store.tasks
        self.stat_vars["Total"].set(str(len(all_tasks)))
        self.stat_vars["Pendientes"].set(str(sum(not task.completed for task in all_tasks)))
        self.stat_vars["Completadas"].set(str(sum(task.completed for task in all_tasks)))
        self.stat_vars["Vencidas"].set(
            str(sum(not task.completed and bool(task.due_date) and task.due_date < today for task in all_tasks))
        )
        visible = len(self.tree.get_children())
        self.status_var.set(f"Mostrando {visible} de {len(all_tasks)} tareas")
        self._show_details()

    def _sort_by(self, column: str) -> None:
        if self.sort_column == column:
            self.sort_descending = not self.sort_descending
        else:
            self.sort_column = column
            self.sort_descending = False
        self.refresh()

    def _selected_task(self) -> Optional[Task]:
        selection = self.tree.selection()
        if not selection:
            return None
        task_id = selection[0]
        return next((task for task in self.store.tasks if task.id == task_id), None)

    def _show_details(self, _event: Optional[tk.Event] = None) -> None:
        task = self._selected_task()
        if task is None:
            self.detail_var.set("Selecciona una tarea para ver su descripcion.")
            return
        due = task.due_date or "Sin fecha limite"
        description = task.description or "Sin descripcion."
        self.detail_var.set(f"{task.title}  |  {task.priority}  |  {due}\n{description}")

    def _open_dialog(self, task: Optional[Task] = None) -> Optional[Dict[str, str]]:
        dialog = TaskDialog(self.root, task)
        self.root.wait_window(dialog)
        return dialog.result

    def _handle_store_error(self, error: OSError) -> None:
        messagebox.showerror("No se pudo guardar", f"Los cambios no se guardaron.\n{error}", parent=self.root)

    def add_task(self) -> None:
        values = self._open_dialog()
        if values is None:
            return
        try:
            task = self.store.add(**values)
        except OSError as error:
            self._handle_store_error(error)
            return
        self.refresh()
        self.tree.selection_set(task.id)
        self.tree.focus(task.id)
        self.status_var.set("Tarea guardada")

    def edit_task(self) -> None:
        task = self._selected_task()
        if task is None:
            messagebox.showinfo("Editar tarea", "Selecciona una tarea primero.", parent=self.root)
            return
        values = self._open_dialog(task)
        if values is None:
            return
        try:
            self.store.update(task.id, values)
        except OSError as error:
            self._handle_store_error(error)
            return
        self.refresh()
        if self.tree.exists(task.id):
            self.tree.selection_set(task.id)
        self.status_var.set("Tarea actualizada")

    def toggle_task(self) -> None:
        task = self._selected_task()
        if task is None:
            messagebox.showinfo("Estado de tarea", "Selecciona una tarea primero.", parent=self.root)
            return
        try:
            self.store.toggle(task.id)
        except OSError as error:
            self._handle_store_error(error)
            return
        self.refresh()
        self.status_var.set("Estado actualizado")

    def delete_task(self) -> None:
        task = self._selected_task()
        if task is None:
            return
        if not messagebox.askyesno("Eliminar tarea", f"¿Eliminar '{task.title}'?", parent=self.root):
            return
        try:
            self.store.delete(task.id)
        except OSError as error:
            self._handle_store_error(error)
            return
        self.refresh()
        self.status_var.set("Tarea eliminada")

    def export_csv(self) -> None:
        if not self.store.tasks:
            messagebox.showinfo("Exportar", "No hay tareas para exportar.", parent=self.root)
            return
        destination = filedialog.asksaveasfilename(
            parent=self.root,
            title="Exportar tareas",
            defaultextension=".csv",
            filetypes=(("Archivo CSV", "*.csv"),),
            initialfile="mis_tareas.csv",
        )
        if not destination:
            return
        try:
            with open(destination, "w", newline="", encoding="utf-8-sig") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=("titulo", "descripcion", "fecha_limite", "prioridad", "estado", "creada"),
                )
                writer.writeheader()
                for task in self.store.tasks:
                    writer.writerow(
                        {
                            "titulo": task.title,
                            "descripcion": task.description,
                            "fecha_limite": task.due_date,
                            "prioridad": task.priority,
                            "estado": "Completada" if task.completed else "Pendiente",
                            "creada": task.created_at,
                        }
                    )
        except OSError as error:
            messagebox.showerror("Error al exportar", str(error), parent=self.root)
            return
        self.status_var.set(f"CSV exportado: {destination}")


def main() -> None:
    root = ttk.Window(themename="flatly")
    try:
        store = TaskStore(DATA_FILE)
    except (OSError, ValueError) as error:
        messagebox.showerror("Error con los datos", str(error), parent=root)
        root.destroy()
        return
    OrganizerApp(root, store)
    root.mainloop()


if __name__ == "__main__":
    main()