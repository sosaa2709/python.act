import json
import random
import time
import tkinter as tk
from pathlib import Path


TILE_SIZE = 32
COLUMNS = 15
ROWS = 13
BOARD_WIDTH = COLUMNS * TILE_SIZE
BOARD_HEIGHT = ROWS * TILE_SIZE
LOOP_MS = 80
BOMB_FUSE = 1.8
FLAME_TIME = 0.45
BLAST_RANGE = 2
PLAYER_START = (1, 1)
ENEMY_STARTS = [(13, 1), (13, 9), (7, 5)]
EXIT_CELL = (13, 11)

BACKGROUND = "#11191c"
BOARD = "#0b1113"
GRID = "#20302d"
PANEL = "#192522"
TEXT = "#f2f4e8"
MUTED = "#92a29b"
MINT = "#a8ef70"
GOLD = "#ffc65c"
BRICK = "#9a5939"
BRICK_EDGE = "#d28a57"
WALL = "#273536"
FLAME = "#ff704d"


class Bomberman:
    def __init__(self, root):
        self.root = root
        self.root.title("Bomberman: Bloque final")
        self.root.geometry("650x610")
        self.root.resizable(False, False)
        self.root.configure(bg=BACKGROUND)
        self.record_path = Path(__file__).with_name("bomberman_record.json")
        self.best_score = self.load_best_score()

        header = tk.Frame(root, bg=BACKGROUND)
        header.pack(fill="x", padx=24, pady=(16, 10))

        title_block = tk.Frame(header, bg=BACKGROUND)
        title_block.pack(side="left")
        tk.Label(
            title_block,
            text="BOMBERMAN",
            font=("Segoe UI", 20, "bold"),
            fg=TEXT,
            bg=BACKGROUND,
        ).pack(anchor="w")
        tk.Label(
            title_block,
            text="BLOQUE FINAL  /  ARCADE",
            font=("Segoe UI", 8, "bold"),
            fg=MUTED,
            bg=BACKGROUND,
        ).pack(anchor="w", pady=(1, 0))

        hud = tk.Frame(header, bg=BACKGROUND)
        hud.pack(side="right")
        self.score_label = self.make_hud(hud, "PUNTOS", MINT)
        self.lives_label = self.make_hud(hud, "VIDAS", GOLD)
        self.enemies_label = self.make_hud(hud, "ENEMIGOS", FLAME)

        self.canvas = tk.Canvas(
            root,
            width=BOARD_WIDTH,
            height=BOARD_HEIGHT,
            bg=BOARD,
            highlightthickness=1,
            highlightbackground=GRID,
        )
        self.canvas.pack(padx=24)

        footer = tk.Frame(root, bg=BACKGROUND)
        footer.pack(fill="x", padx=24, pady=(10, 16))
        controls = tk.Frame(footer, bg=BACKGROUND)
        controls.pack(side="left")
        tk.Label(
            controls,
            text="FLECHAS / WASD: MOVER   ·   ESPACIO: BOMBA   ·   P: PAUSA",
            font=("Segoe UI", 8, "bold"),
            fg=MUTED,
            bg=BACKGROUND,
        ).pack(anchor="w")
        tk.Label(
            controls,
            text="Eliminá a los enemigos y encontrá la salida.",
            font=("Segoe UI", 9),
            fg=TEXT,
            bg=BACKGROUND,
        ).pack(anchor="w", pady=(3, 0))

        tk.Button(
            footer,
            text="NUEVA PARTIDA  ·  R",
            command=self.restart,
            font=("Segoe UI", 9, "bold"),
            fg=BACKGROUND,
            bg=MINT,
            activeforeground=BACKGROUND,
            activebackground=GOLD,
            relief="flat",
            padx=13,
            pady=10,
            cursor="hand2",
        ).pack(side="right")

        self.root.bind_all("<KeyPress>", self.on_key)
        self.loop_id = None
        self.restart()

    def make_hud(self, parent, title, color):
        card = tk.Frame(parent, bg=PANEL, padx=10, pady=5)
        card.pack(side="left", padx=(6, 0))
        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 7, "bold"),
            fg=MUTED,
            bg=PANEL,
        ).pack(anchor="e")
        value = tk.Label(
            card,
            text="0",
            font=("Segoe UI", 12, "bold"),
            fg=color,
            bg=PANEL,
        )
        value.pack(anchor="e")
        return value

    def load_best_score(self):
        try:
            with self.record_path.open("r", encoding="utf-8") as record_file:
                data = json.load(record_file)
            score = data.get("best_score", 0) if isinstance(data, dict) else 0
            return score if isinstance(score, int) and score >= 0 else 0
        except (json.JSONDecodeError, OSError, TypeError):
            return 0

    def save_best_score(self):
        try:
            with self.record_path.open("w", encoding="utf-8") as record_file:
                json.dump({"best_score": self.best_score}, record_file, indent=4)
        except OSError:
            pass

    def restart(self):
        if self.loop_id is not None:
            self.root.after_cancel(self.loop_id)
            self.loop_id = None

        self.hard_walls = {
            (x, y)
            for x in range(COLUMNS)
            for y in range(ROWS)
            if x == 0
            or y == 0
            or x == COLUMNS - 1
            or y == ROWS - 1
            or (x % 2 == 0 and y % 2 == 0)
        }
        self.player = PLAYER_START
        self.enemies = list(ENEMY_STARTS)
        self.bricks = self.make_bricks()
        self.bricks.add(EXIT_CELL)
        self.bombs = {}
        self.flames = {}
        self.score = 0
        self.lives = 3
        self.running = True
        self.paused = False
        self.won = False
        self.invulnerable_until = 0.0
        self.next_enemy_move = time.monotonic() + 0.55
        self.draw_board()
        self.draw()
        self.schedule_loop()

    def make_bricks(self):
        protected = set()
        for origin in [PLAYER_START, EXIT_CELL, *ENEMY_STARTS]:
            protected.add(origin)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                neighbor = (origin[0] + dx, origin[1] + dy)
                if 0 < neighbor[0] < COLUMNS - 1 and 0 < neighbor[1] < ROWS - 1:
                    protected.add(neighbor)

        bricks = set()
        for y in range(1, ROWS - 1):
            for x in range(1, COLUMNS - 1):
                cell = (x, y)
                if cell not in self.hard_walls and cell not in protected:
                    if random.random() < 0.29:
                        bricks.add(cell)
        return bricks

    def draw_board(self):
        self.canvas.delete("world")
        for x in range(0, BOARD_WIDTH + 1, TILE_SIZE):
            self.canvas.create_line(x, 0, x, BOARD_HEIGHT, fill=GRID, tags="world")
        for y in range(0, BOARD_HEIGHT + 1, TILE_SIZE):
            self.canvas.create_line(0, y, BOARD_WIDTH, y, fill=GRID, tags="world")

        for x, y in self.hard_walls:
            left, top, right, bottom = self.tile_bounds((x, y), 1)
            self.canvas.create_rectangle(
                left,
                top,
                right,
                bottom,
                fill=WALL,
                outline="#3b4e4e",
                width=1,
                tags="world",
            )
            self.canvas.create_line(
                left + 4,
                top + 5,
                right - 4,
                top + 5,
                fill="#4a5c5a",
                width=2,
                tags="world",
            )

        for x, y in self.bricks:
            left, top, right, bottom = self.tile_bounds((x, y), 3)
            self.canvas.create_rectangle(
                left,
                top,
                right,
                bottom,
                fill=BRICK,
                outline=BRICK_EDGE,
                width=1,
                tags="world",
            )
            self.canvas.create_line(
                left + 2,
                top + 10,
                right - 2,
                top + 10,
                fill="#633c2e",
                tags="world",
            )
            self.canvas.create_line(
                left + 10,
                top + 2,
                left + 10,
                top + 10,
                fill=BRICK_EDGE,
                tags="world",
            )
            self.canvas.create_line(
                right - 10,
                top + 10,
                right - 10,
                bottom - 2,
                fill=BRICK_EDGE,
                tags="world",
            )

        if not self.enemies and EXIT_CELL not in self.bricks:
            left, top, right, bottom = self.tile_bounds(EXIT_CELL, 3)
            self.canvas.create_rectangle(
                left,
                top,
                right,
                bottom,
                fill="#355a38",
                outline=MINT,
                width=2,
                tags="world",
            )
            self.canvas.create_text(
                (left + right) / 2,
                (top + bottom) / 2,
                text="SALIDA",
                fill=TEXT,
                font=("Segoe UI", 6, "bold"),
                tags="world",
            )

    def tile_bounds(self, cell, padding=0):
        x, y = cell
        return (
            x * TILE_SIZE + padding,
            y * TILE_SIZE + padding,
            (x + 1) * TILE_SIZE - padding,
            (y + 1) * TILE_SIZE - padding,
        )

    def on_key(self, event):
        key = event.keysym.lower()
        if key == "r":
            self.restart()
            return "break"
        if key == "p":
            self.toggle_pause()
            return "break"
        if key == "space":
            self.place_bomb()
            return "break"
        if self.paused or not self.running:
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
        direction = directions.get(key)
        if direction is not None:
            self.move_player(*direction)
            return "break"

    def move_player(self, dx, dy):
        if self.paused or not self.running:
            return
        destination = (self.player[0] + dx, self.player[1] + dy)
        if (
            destination in self.hard_walls
            or destination in self.bricks
            or destination in self.bombs
        ):
            return

        self.player = destination
        now = time.monotonic()
        if self.flames.get(destination, 0) > now:
            self.hit_player(now)
        if not self.enemies and EXIT_CELL not in self.bricks and self.player == EXIT_CELL:
            self.won = True
            self.running = False
        self.draw()

    def place_bomb(self):
        if self.paused or not self.running or len(self.bombs) >= 2:
            return
        if self.player not in self.bombs:
            self.bombs[self.player] = time.monotonic() + BOMB_FUSE
            self.draw()

    def toggle_pause(self):
        if not self.running:
            return
        now = time.monotonic()
        self.paused = not self.paused
        if self.paused:
            self.pause_started = now
        else:
            paused_for = now - self.pause_started
            self.bombs = {cell: deadline + paused_for for cell, deadline in self.bombs.items()}
            self.flames = {cell: deadline + paused_for for cell, deadline in self.flames.items()}
            self.next_enemy_move += paused_for
        self.draw()

    def schedule_loop(self):
        if self.running and self.loop_id is None:
            self.loop_id = self.root.after(LOOP_MS, self.game_loop)

    def game_loop(self):
        self.loop_id = None
        if not self.running:
            return
        if not self.paused:
            now = time.monotonic()
            self.flames = {
                cell: deadline
                for cell, deadline in self.flames.items()
                if deadline > now
            }
            self.explode_due_bombs(now)
            if self.running and now >= self.next_enemy_move:
                self.move_enemies(now)
                self.next_enemy_move = now + 0.43
            self.draw()
        self.schedule_loop()

    def explode_due_bombs(self, now):
        pending = [cell for cell, deadline in self.bombs.items() if deadline <= now]
        if not pending:
            return

        affected_cells = set()
        changed_world = False
        previous_enemy_count = len(self.enemies)
        while pending:
            bomb = pending.pop()
            if bomb not in self.bombs:
                continue
            self.bombs.pop(bomb)
            affected_cells.add(bomb)

            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                for distance in range(1, BLAST_RANGE + 1):
                    cell = (bomb[0] + dx * distance, bomb[1] + dy * distance)
                    if cell in self.hard_walls:
                        break
                    affected_cells.add(cell)
                    if cell in self.bombs and cell not in pending:
                        pending.append(cell)
                    if cell in self.bricks:
                        self.bricks.remove(cell)
                        self.add_score(10)
                        changed_world = True
                        break

        now = time.monotonic()
        for cell in affected_cells:
            self.flames[cell] = now + FLAME_TIME
            if cell in self.enemies:
                self.enemies.remove(cell)
                self.add_score(100)

        if len(self.enemies) != previous_enemy_count:
            changed_world = True
        if changed_world:
            self.draw_board()
        if self.player in affected_cells:
            self.hit_player(now)

    def move_enemies(self, now):
        occupied = set(self.enemies)
        moved_enemies = []
        for enemy in self.enemies:
            occupied.discard(enemy)
            options = []
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                cell = (enemy[0] + dx, enemy[1] + dy)
                if (
                    cell not in self.hard_walls
                    and cell not in self.bricks
                    and cell not in self.bombs
                    and cell not in self.flames
                    and cell not in occupied
                ):
                    options.append(cell)

            destination = enemy
            if options:
                closer = [
                    cell
                    for cell in options
                    if abs(cell[0] - self.player[0]) + abs(cell[1] - self.player[1])
                    < abs(enemy[0] - self.player[0]) + abs(enemy[1] - self.player[1])
                ]
                destination = random.choice(closer or options)

            if destination == self.player:
                self.hit_player(now)
            moved_enemies.append(destination)
            occupied.add(destination)
        self.enemies = moved_enemies
        self.draw()

    def hit_player(self, now):
        if now < self.invulnerable_until or not self.running:
            return
        self.lives -= 1
        if self.lives <= 0:
            self.running = False
            return
        self.player = PLAYER_START
        self.invulnerable_until = now + 1.4

    def add_score(self, points):
        self.score += points
        if self.score > self.best_score:
            self.best_score = self.score
            self.save_best_score()

    def draw(self):
        self.canvas.delete("actors")
        self.score_label.config(text=f"{self.score:04d}")
        self.lives_label.config(text=str(max(0, self.lives)))
        self.enemies_label.config(text=str(len(self.enemies)))
        now = time.monotonic()

        for (x, y), deadline in self.bombs.items():
            left, top, right, bottom = self.tile_bounds((x, y), 5)
            pulse = int(max(0, deadline - now) * 8) % 2
            self.canvas.create_oval(
                left,
                top,
                right,
                bottom,
                fill="#39241e",
                outline=GOLD if pulse else FLAME,
                width=2,
                tags="actors",
            )
            self.canvas.create_oval(
                left + 8,
                top + 8,
                right - 8,
                bottom - 8,
                fill=FLAME if pulse else GOLD,
                outline="",
                tags="actors",
            )

        for x, y in self.flames:
            left, top, right, bottom = self.tile_bounds((x, y), 2)
            self.canvas.create_rectangle(
                left,
                top,
                right,
                bottom,
                fill=FLAME,
                outline=GOLD,
                width=2,
                tags="actors",
            )
            self.canvas.create_oval(
                left + 8,
                top + 8,
                right - 8,
                bottom - 8,
                fill="#fff2a8",
                outline="",
                tags="actors",
            )

        for x, y in self.enemies:
            left, top, right, bottom = self.tile_bounds((x, y), 5)
            self.canvas.create_oval(
                left,
                top,
                right,
                bottom,
                fill="#c4453f",
                outline="#ff9274",
                width=2,
                tags="actors",
            )
            self.canvas.create_oval(
                left + 5,
                top + 8,
                left + 10,
                top + 13,
                fill=TEXT,
                outline="",
                tags="actors",
            )
            self.canvas.create_oval(
                right - 10,
                top + 8,
                right - 5,
                top + 13,
                fill=TEXT,
                outline="",
                tags="actors",
            )

        if now >= self.invulnerable_until or int(now * 10) % 2:
            left, top, right, bottom = self.tile_bounds(self.player, 5)
            self.canvas.create_oval(
                left,
                top,
                right,
                bottom,
                fill="#e9d5a7",
                outline=TEXT,
                width=2,
                tags="actors",
            )
            self.canvas.create_rectangle(
                left + 3,
                top + 14,
                right - 3,
                bottom - 2,
                fill="#4da77b",
                outline="",
                tags="actors",
            )
            self.canvas.create_rectangle(
                left + 5,
                top + 8,
                right - 5,
                top + 14,
                fill="#243534",
                outline="",
                tags="actors",
            )

        if self.paused:
            self.draw_overlay("PAUSA", "Pulsa P para continuar")
        elif not self.running:
            if self.won:
                self.draw_overlay("¡NIVEL COMPLETADO!", f"Puntuación: {self.score}  ·  Pulsa R")
            else:
                self.draw_overlay("FIN DE PARTIDA", f"Puntuación: {self.score}  ·  Pulsa R")

    def draw_overlay(self, title, subtitle):
        self.canvas.create_rectangle(
            48,
            150,
            BOARD_WIDTH - 48,
            266,
            fill=PANEL,
            outline=MINT,
            width=2,
            tags="actors",
        )
        self.canvas.create_text(
            BOARD_WIDTH // 2,
            194,
            text=title,
            fill=MINT,
            font=("Segoe UI", 18, "bold"),
            tags="actors",
        )
        self.canvas.create_text(
            BOARD_WIDTH // 2,
            232,
            text=subtitle,
            fill=TEXT,
            font=("Segoe UI", 9),
            tags="actors",
        )


if __name__ == "__main__":
    main_window = tk.Tk()
    Bomberman(main_window)
    main_window.mainloop()