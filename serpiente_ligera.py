import json
import random
import tkinter as tk
import time
from pathlib import Path
from tkinter import messagebox


CELL_SIZE = 20
COLUMNS = 25
ROWS = 20
BOARD_WIDTH = CELL_SIZE * COLUMNS
BOARD_HEIGHT = CELL_SIZE * ROWS
TICK_MS = 125
FRAME_MS = 16
LEVEL_SCORE = 50

DIFFICULTIES = {
    "suave": {"label": "TRANQUI", "detail": "Más tiempo", "speed": 165},
    "normal": {"label": "NORMAL", "detail": "Equilibrado", "speed": 125},
    "rapido": {"label": "RÁPIDO", "detail": "Más veloz", "speed": 95},
    "imposible": {"label": "IMPOSIBLE", "detail": "Sin margen", "speed": 60},
}

BACKGROUND = "#11191c"
BOARD = "#0b1113"
GRID = "#203322"
PANEL = "#19271b"
TEXT = "#f2f4e8"
MUTED = "#91a09d"
SNAKE = "#a8ef24"
HEAD = "#dcff69"
TOXIC_GLOW = "#537b1d"
TOXIC_CORE = "#efffa0"
FOOD = "#ff8066"


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Serpiente")
        self.root.geometry("600x650")
        self.root.configure(bg=BACKGROUND)
        self.root.resizable(False, False)
        self.record_path = Path(__file__).with_name("serpiente_record.json")
        self.difficulty = tk.StringVar(root, value="normal")
        self.best_score = self.load_best_score()
        self.in_game = False

        self.menu_frame = tk.Frame(root, bg=BACKGROUND)
        self.game_frame = tk.Frame(root, bg=BACKGROUND)

        header = tk.Frame(self.game_frame, bg=BACKGROUND)
        header.pack(fill="x", padx=20, pady=(16, 10))

        title_block = tk.Frame(header, bg=BACKGROUND)
        title_block.pack(side="left", pady=2)

        tk.Label(
            title_block,
            text="SERPIENTE",
            font=("Segoe UI", 19, "bold"),
            fg=TEXT,
            bg=BACKGROUND,
        ).pack(anchor="w")
        tk.Label(
            title_block,
            text="ARCADE CLÁSICO",
            font=("Segoe UI", 8, "bold"),
            fg=MUTED,
            bg=BACKGROUND,
        ).pack(anchor="w", pady=(1, 0))

        score_block = tk.Frame(header, bg=BACKGROUND)
        score_block.pack(side="right")
        self.level_label = self.make_score_card(score_block, "NIVEL", FOOD)
        self.score_label = self.make_score_card(score_block, "PUNTOS", HEAD)
        self.best_label = self.make_score_card(score_block, "RÉCORD", FOOD)

        self.canvas = tk.Canvas(
            self.game_frame,
            width=BOARD_WIDTH,
            height=BOARD_HEIGHT,
            bg=BOARD,
            highlightthickness=1,
            highlightbackground=GRID,
        )
        self.canvas.pack(padx=20)
        self.draw_grid()

        footer = tk.Frame(self.game_frame, bg=BACKGROUND)
        footer.pack(fill="x", padx=20, pady=(10, 16))

        controls = tk.Frame(footer, bg=BACKGROUND)
        controls.pack(side="left")
        tk.Label(
            controls,
            text="MOVER",
            font=("Segoe UI", 8, "bold"),
            fg=MUTED,
            bg=BACKGROUND,
        ).pack(anchor="w")
        tk.Label(
            controls,
            text="Flechas / WASD   ·   Espacio pausa",
            font=("Segoe UI", 9),
            fg=TEXT,
            bg=BACKGROUND,
        ).pack(anchor="w", pady=(2, 0))

        footer_buttons = tk.Frame(footer, bg=BACKGROUND)
        footer_buttons.pack(side="right")
        tk.Button(
            footer_buttons,
            text="MENÚ",
            command=self.show_menu,
            font=("Segoe UI", 9, "bold"),
            fg=TEXT,
            bg=PANEL,
            activeforeground=TEXT,
            activebackground=GRID,
            relief="flat",
            padx=11,
            pady=9,
            cursor="hand2",
        ).pack(side="left", padx=(0, 6))
        tk.Button(
            footer_buttons,
            text="REINICIAR  ·  R",
            command=self.restart,
            font=("Segoe UI", 9, "bold"),
            fg=BACKGROUND,
            bg=HEAD,
            activeforeground=BACKGROUND,
            activebackground=SNAKE,
            relief="flat",
            padx=13,
            pady=9,
            cursor="hand2",
        ).pack(side="right")

        self.root.bind_all("<KeyPress>", self.on_key)
        self.move_after_id = None
        self.animation_after_id = None
        self.previous_snake = []
        self.animation_progress = 1.0
        self.animation_started = 0.0
        self.animation_duration = TICK_MS / 1000
        self.move_interval_ms = TICK_MS
        self.build_menu()
        self.menu_frame.pack(fill="both", expand=True, padx=22, pady=18)

    def make_score_card(self, parent, title, color):
        card = tk.Frame(parent, bg=PANEL, padx=11, pady=5)
        card.pack(side="left", padx=(7, 0))
        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 7, "bold"),
            fg=MUTED,
            bg=PANEL,
        ).pack(anchor="e")
        value = tk.Label(
            card,
            text="000",
            font=("Segoe UI", 12, "bold"),
            fg=color,
            bg=PANEL,
        )
        value.pack(anchor="e")
        return value

    def build_menu(self):
        heading = tk.Frame(self.menu_frame, bg=BACKGROUND)
        heading.pack(fill="x", pady=(8, 12))
        tk.Label(
            heading,
            text="ARCADE  /  01",
            font=("Segoe UI", 9, "bold"),
            fg=FOOD,
            bg=BACKGROUND,
        ).pack(anchor="w")
        tk.Label(
            heading,
            text="SERPIENTE",
            font=("Segoe UI", 31, "bold"),
            fg=TEXT,
            bg=BACKGROUND,
        ).pack(anchor="w", pady=(2, 0))
        tk.Label(
            heading,
            text="Come, crece y no te cruces en tu camino.",
            font=("Segoe UI", 11),
            fg=MUTED,
            bg=BACKGROUND,
        ).pack(anchor="w", pady=(0, 4))

        preview = tk.Canvas(
            self.menu_frame,
            width=BOARD_WIDTH,
            height=92,
            bg=BOARD,
            highlightthickness=1,
            highlightbackground=GRID,
        )
        preview.pack(fill="x", pady=(0, 14))
        preview.create_line(0, 23, BOARD_WIDTH, 23, fill=GRID)
        preview.create_line(0, 46, BOARD_WIDTH, 46, fill=GRID)
        preview.create_line(0, 69, BOARD_WIDTH, 69, fill=GRID)
        preview.create_line(70, 46, 270, 46, fill=SNAKE, width=14, capstyle="round")
        for x in (70, 95, 120, 145, 170, 195, 220, 245, 270):
            preview.create_oval(x - 8, 38, x + 8, 54, fill=HEAD if x == 270 else SNAKE, outline="")
        preview.create_oval(379, 34, 403, 58, outline=FOOD, width=2)
        preview.create_oval(386, 41, 396, 51, fill=FOOD, outline="")
        self.menu_record_label = tk.Label(
            self.menu_frame,
            text=f"RÉCORD PERSONAL     {self.best_score:03d}",
            font=("Segoe UI", 9, "bold"),
            fg=HEAD,
            bg=BACKGROUND,
        )
        self.menu_record_label.pack(anchor="e", pady=(0, 12))

        difficulty_panel = tk.Frame(
            self.menu_frame,
            bg=PANEL,
            padx=15,
            pady=13,
            highlightthickness=1,
            highlightbackground=GRID,
        )
        difficulty_panel.pack(fill="x")
        tk.Label(
            difficulty_panel,
            text="ELEGÍ TU RITMO",
            font=("Segoe UI", 9, "bold"),
            fg=MUTED,
            bg=PANEL,
        ).pack(anchor="w", pady=(0, 9))

        choices = tk.Frame(difficulty_panel, bg=PANEL)
        choices.pack(fill="x")
        self.difficulty_buttons = {}
        for key, option in DIFFICULTIES.items():
            button = tk.Button(
                choices,
                text=f"{option['label']}\n{option['detail']}",
                command=lambda selected=key: self.select_difficulty(selected),
                font=("Segoe UI", 9, "bold"),
                fg=TEXT,
                bg=BACKGROUND,
                activeforeground=TEXT,
                activebackground=GRID,
                relief="flat",
                padx=11,
                pady=9,
                cursor="hand2",
            )
            button.pack(side="left", fill="x", expand=True, padx=(0, 7))
            self.difficulty_buttons[key] = button
        self.select_difficulty(self.difficulty.get())

        tk.Label(
            self.menu_frame,
            text="Cada 50 puntos subís de nivel. Los bloques nuevos no perdonan.",
            font=("Segoe UI", 9),
            fg=MUTED,
            bg=BACKGROUND,
            wraplength=470,
        ).pack(anchor="w", pady=(13, 15))

        tk.Button(
            self.menu_frame,
            text="JUGAR  →",
            command=self.start_game,
            font=("Segoe UI", 11, "bold"),
            fg=BACKGROUND,
            bg=HEAD,
            activeforeground=BACKGROUND,
            activebackground=SNAKE,
            relief="flat",
            padx=18,
            pady=12,
            cursor="hand2",
        ).pack(fill="x")

        tk.Label(
            self.menu_frame,
            text="FLECHAS / WASD PARA MOVER   ·   ESPACIO PARA PAUSAR",
            font=("Segoe UI", 8, "bold"),
            fg=MUTED,
            bg=BACKGROUND,
        ).pack(pady=(13, 0))

    def select_difficulty(self, difficulty):
        self.difficulty.set(difficulty)
        for key, button in self.difficulty_buttons.items():
            selected = key == difficulty
            button.configure(
                bg="#29423a" if selected else BACKGROUND,
                fg=HEAD if selected else TEXT,
                activebackground="#29423a" if selected else GRID,
            )

    def start_game(self):
        self.in_game = True
        self.menu_frame.pack_forget()
        self.game_frame.pack(fill="both", expand=True)
        self.restart()

    def show_menu(self):
        for attribute in ("move_after_id", "animation_after_id"):
            callback_id = getattr(self, attribute, None)
            if callback_id is not None:
                self.root.after_cancel(callback_id)
                setattr(self, attribute, None)
        self.running = False
        self.paused = False
        self.in_game = False
        self.game_frame.pack_forget()
        self.menu_frame.pack(fill="both", expand=True, padx=22, pady=18)
        self.menu_record_label.config(text=f"RÉCORD PERSONAL     {self.best_score:03d}")

    def load_best_score(self):
        try:
            with self.record_path.open("r", encoding="utf-8") as record_file:
                data = json.load(record_file)
            if not isinstance(data, dict):
                return 0
            score = data.get("best_score", 0)
            return score if isinstance(score, int) and score >= 0 else 0
        except (json.JSONDecodeError, OSError, TypeError):
            return 0

    def save_best_score(self):
        try:
            with self.record_path.open("w", encoding="utf-8") as record_file:
                json.dump({"best_score": self.best_score}, record_file, indent=4)
        except OSError as error:
            messagebox.showwarning(
                "Récord no guardado",
                f"No se pudo guardar el récord.\n{error}",
                parent=self.root,
            )

    def draw_grid(self):
        for x in range(0, BOARD_WIDTH, CELL_SIZE):
            self.canvas.create_line(x, 0, x, BOARD_HEIGHT, fill=GRID)
        for y in range(0, BOARD_HEIGHT, CELL_SIZE):
            self.canvas.create_line(0, y, BOARD_WIDTH, y, fill=GRID)

    def restart(self):
        if self.move_after_id is not None:
            self.root.after_cancel(self.move_after_id)
        if self.animation_after_id is not None:
            self.root.after_cancel(self.animation_after_id)
        self.move_after_id = None
        self.animation_after_id = None

        self.snake = [(COLUMNS // 2, ROWS // 2), (COLUMNS // 2 - 1, ROWS // 2)]
        self.previous_snake = list(self.snake)
        self.obstacles = []
        self.level = 1
        self.direction = (1, 0)
        self.next_direction = self.direction
        self.score = 0
        self.running = True
        self.paused = False
        self.won = False
        self.animation_progress = 1.0
        self.move_interval_ms = self.get_move_speed()
        self.animation_duration = self.move_interval_ms / 1000
        self.food = self.place_food()
        self.draw()
        self.schedule_tick()

    def place_food(self):
        occupied = set(self.snake) | set(self.obstacles)
        empty_cells = [
            (x, y)
            for x in range(COLUMNS)
            for y in range(ROWS)
            if (x, y) not in occupied
        ]
        return random.choice(empty_cells) if empty_cells else None

    def add_obstacles(self, count):
        occupied = set(self.snake) | set(self.obstacles)
        if self.food is not None:
            occupied.add(self.food)
        head_x, head_y = self.snake[0]
        available = [
            (x, y)
            for x in range(COLUMNS)
            for y in range(ROWS)
            if (x, y) not in occupied and abs(x - head_x) + abs(y - head_y) >= 4
        ]
        if len(available) < count:
            available = [
                (x, y)
                for x in range(COLUMNS)
                for y in range(ROWS)
                if (x, y) not in occupied
            ]
        self.obstacles.extend(random.sample(available, min(count, len(available))))

    def on_key(self, event):
        key = event.keysym.lower()

        if key in ("return", "kp_enter") and not self.in_game:
            self.start_game()
            return "break"

        if key == "r":
            if self.in_game:
                self.restart()
            else:
                self.start_game()
            return "break"

        if key == "m" and self.in_game:
            self.show_menu()
            return "break"

        if key == "space" and self.in_game:
            self.toggle_pause()
            return "break"

        if not self.in_game:
            return

        directions = {
            "up": (0, -1),
            "w": (0, -1),
            "down": (0, 1),
            "s": (0, 1),
            "left": (-1, 0),
            "a": (-1, 0),
            "right": (1, 0),
            "d": (1, 0),
        }
        new_direction = directions.get(key)
        if new_direction is None or not self.running or self.paused:
            return

        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.next_direction = new_direction
        return "break"

    def toggle_pause(self):
        if not self.running:
            return

        self.paused = not self.paused
        if self.paused:
            self.update_animation_progress()
            if self.move_after_id is not None:
                self.root.after_cancel(self.move_after_id)
                self.move_after_id = None
            if self.animation_after_id is not None:
                self.root.after_cancel(self.animation_after_id)
                self.animation_after_id = None
        else:
            self.animation_started = (
                time.perf_counter() - self.animation_progress * self.animation_duration
            )
            self.schedule_tick()
            self.schedule_animation()
        self.draw()

    def schedule_tick(self):
        if self.running and not self.paused:
            self.move_interval_ms = self.get_move_speed()
            self.move_after_id = self.root.after(self.move_interval_ms, self.tick)

    def get_move_speed(self):
        difficulty = self.difficulty.get()
        base_speed = DIFFICULTIES[difficulty]["speed"]
        minimum_speed = 38 if difficulty == "imposible" else 60
        return max(minimum_speed, base_speed - (self.level - 1) * 7)

    def schedule_animation(self):
        if (
            self.running
            and not self.paused
            and self.animation_progress < 1.0
            and self.animation_after_id is None
        ):
            self.animation_after_id = self.root.after(FRAME_MS, self.animate)

    def update_animation_progress(self):
        if self.animation_progress < 1.0:
            elapsed = time.perf_counter() - self.animation_started
            self.animation_progress = min(1.0, elapsed / self.animation_duration)

    def animate(self):
        self.animation_after_id = None
        if not self.running or self.paused:
            return

        self.update_animation_progress()
        self.draw()
        self.schedule_animation()

    def tick(self):
        self.move_after_id = None
        if not self.running or self.paused:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        move_x, move_y = self.direction
        new_head = (head_x + move_x, head_y + move_y)
        eating = new_head == self.food
        body_to_check = self.snake if eating else self.snake[:-1]

        hit_wall = not (
            0 <= new_head[0] < COLUMNS and 0 <= new_head[1] < ROWS
        )
        if hit_wall or new_head in body_to_check or new_head in self.obstacles:
            self.running = False
            self.animation_progress = 1.0
            self.draw()
            return

        self.previous_snake = list(self.snake)
        if eating:
            self.previous_snake.append(self.snake[-1])
        self.snake.insert(0, new_head)
        if eating:
            self.score += 10
            if self.score > self.best_score:
                self.best_score = self.score
                self.save_best_score()
            next_level = self.score // LEVEL_SCORE + 1
            if next_level > self.level:
                self.level = next_level
                if self.difficulty.get() == "imposible":
                    obstacle_count = min(8, 3 + self.level // 2)
                else:
                    obstacle_count = min(5, 2 + self.level // 3)
                self.add_obstacles(obstacle_count)
            self.food = self.place_food()
            if self.food is None:
                self.running = False
                self.won = True
        else:
            self.snake.pop()

        self.animation_progress = 0.0
        self.animation_started = time.perf_counter()
        self.animation_duration = self.move_interval_ms / 1000
        self.draw(0.0)
        self.schedule_tick()
        self.schedule_animation()

    def draw(self, progress=None):
        self.canvas.delete("dynamic")
        self.score_label.config(text=f"{self.score:03d}")
        self.best_label.config(text=f"{self.best_score:03d}")
        self.level_label.config(text=f"{self.level:02d}")

        if progress is None:
            progress = self.animation_progress

        if self.food is not None:
            x, y = self.food
            padding = 3
            self.canvas.create_oval(
                x * CELL_SIZE + padding,
                y * CELL_SIZE + padding,
                (x + 1) * CELL_SIZE - padding,
                (y + 1) * CELL_SIZE - padding,
                fill="",
                outline=FOOD,
                width=2,
                tags="dynamic",
            )
            self.canvas.create_oval(
                x * CELL_SIZE + 7,
                y * CELL_SIZE + 7,
                (x + 1) * CELL_SIZE - 7,
                (y + 1) * CELL_SIZE - 7,
                fill=FOOD,
                outline="",
                tags="dynamic",
            )

        for x, y in self.obstacles:
            left = x * CELL_SIZE + 3
            top = y * CELL_SIZE + 3
            right = (x + 1) * CELL_SIZE - 3
            bottom = (y + 1) * CELL_SIZE - 3
            self.canvas.create_rectangle(
                left,
                top,
                right,
                bottom,
                fill="#293a38",
                outline="#607b6d",
                width=2,
                tags="dynamic",
            )
            self.canvas.create_line(
                left + 3,
                top + 3,
                right - 3,
                bottom - 3,
                fill="#607b6d",
                width=2,
                tags="dynamic",
            )

        visual_snake = self.get_visual_positions(progress)
        if len(visual_snake) > 1:
            coordinates = [coordinate for point in visual_snake for coordinate in point]
            for color, width in (
                (TOXIC_GLOW, CELL_SIZE + 2),
                (SNAKE, CELL_SIZE - 4),
                (TOXIC_CORE, 3),
            ):
                self.canvas.create_line(
                    *coordinates,
                    fill=color,
                    width=width,
                    capstyle="round",
                    joinstyle="round",
                    tags="dynamic",
                )

        for index, (center_x, center_y) in enumerate(visual_snake):
            radius = CELL_SIZE // 2 - (1 if index == 0 else 2)
            if index == 0:
                self.canvas.create_oval(
                    center_x - radius - 2,
                    center_y - radius - 2,
                    center_x + radius + 2,
                    center_y + radius + 2,
                    fill=TOXIC_GLOW,
                    outline="",
                    tags="dynamic",
                )
            self.canvas.create_oval(
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
                fill=HEAD if index == 0 else SNAKE,
                outline="",
                tags="dynamic",
            )
            if index == 0:
                self.canvas.create_text(
                    center_x,
                    center_y,
                    text="☢",
                    fill=BOARD,
                    font=("Segoe UI Symbol", 11, "bold"),
                    tags="dynamic",
                )

        if self.paused:
            self.draw_message("PAUSA", "Pulsa Espacio para continuar")
        elif not self.running:
            title = "¡Ganaste!" if self.won else "Fin del juego"
            self.draw_message(
                title,
                f"Puntos: {self.score}   ·   Pulsa R para repetir o M para el menú",
            )

    def get_visual_positions(self, progress):
        positions = []
        for index, (end_x, end_y) in enumerate(self.snake):
            if index < len(self.previous_snake):
                start_x, start_y = self.previous_snake[index]
            else:
                start_x, start_y = end_x, end_y

            pixel_start_x = start_x * CELL_SIZE + CELL_SIZE / 2
            pixel_start_y = start_y * CELL_SIZE + CELL_SIZE / 2
            pixel_end_x = end_x * CELL_SIZE + CELL_SIZE / 2
            pixel_end_y = end_y * CELL_SIZE + CELL_SIZE / 2
            x = pixel_start_x + (pixel_end_x - pixel_start_x) * progress
            y = pixel_start_y + (pixel_end_y - pixel_start_y) * progress
            positions.append((x, y))
        return positions

    def draw_eyes(self, center_x, center_y):
        move_x, move_y = self.direction
        if move_x:
            eye_positions = [
                (center_x + move_x * 4, center_y - 4),
                (center_x + move_x * 4, center_y + 4),
            ]
        else:
            eye_positions = [
                (center_x - 4, center_y + move_y * 4),
                (center_x + 4, center_y + move_y * 4),
            ]
        for eye_x, eye_y in eye_positions:
            self.canvas.create_oval(
                eye_x - 1.5,
                eye_y - 1.5,
                eye_x + 1.5,
                eye_y + 1.5,
                fill=BOARD,
                outline="",
                tags="dynamic",
            )

    def draw_message(self, title, subtitle):
        self.canvas.create_rectangle(
            48,
            143,
            BOARD_WIDTH - 48,
            257,
            fill=PANEL,
            outline="#34484a",
            width=2,
            tags="dynamic",
        )
        self.canvas.create_rectangle(
            48,
            143,
            54,
            257,
            fill=HEAD,
            outline="",
            tags="dynamic",
        )
        self.canvas.create_text(
            BOARD_WIDTH // 2,
            183,
            text=title,
            fill=HEAD,
            font=("Segoe UI", 23, "bold"),
            tags="dynamic",
        )
        self.canvas.create_text(
            BOARD_WIDTH // 2,
            222,
            text=subtitle,
            fill=TEXT,
            font=("Segoe UI", 9),
            tags="dynamic",
        )


if __name__ == "__main__":
    window = tk.Tk()
    SnakeGame(window)
    window.mainloop()