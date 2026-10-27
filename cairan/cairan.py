
import tkinter as tk
import math
import ast
import operator

# ---------- COLORS ----------
BG = "#111827"
PANEL = "#1F2937"
KEY = "#374151"
BLUE = "#2563EB"
GREEN = "#10B981"
RED = "#DC5252"
WHITE = "#F9FAFB"
MUTED = "#9CA3AF"


class NexusCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Nexus Scientific Calculator")
        self.root.geometry("650x570")
        self.root.minsize(600, 520)
        self.root.configure(bg=BG)

        self.expression = tk.StringVar()
        self.degrees = True
        self.history = []

        self.build_header()
        self.build_display()
        self.build_keypad()
        self.build_history()

    # ---------- HEADER ----------
    def build_header(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=18, pady=(15, 8))

        tk.Label(
            header,
            text="NEXUS CALC",
            font=("Arial", 20, "bold"),
            bg=BG, fg=WHITE
        ).pack(side="left")

        self.mode_btn = tk.Button(
            header,
            text="DEG",
            command=self.toggle_mode,
            bg=GREEN, fg=BG,
            font=("Arial", 10, "bold"),
            relief="flat", width=7
        )
        self.mode_btn.pack(side="right")

        tk.Label(
            header,
            text="SCIENTIFIC EDITION",
            font=("Arial", 9),
            bg=BG, fg=MUTED
        ).pack(side="right", padx=12)

    # ---------- DISPLAY ----------
    def build_display(self):
        panel = tk.Frame(self.root, bg=PANEL)
        panel.pack(fill="x", padx=18, pady=8)

        tk.Label(
            panel,
            text="EXPRESSION",
            font=("Arial", 9, "bold"),
            bg=PANEL, fg=MUTED
        ).pack(anchor="w", padx=14, pady=(10, 0))

        self.screen = tk.Entry(
            panel,
            textvariable=self.expression,
            font=("Consolas", 25),
            bg=PANEL, fg=WHITE,
            insertbackground=WHITE,
            relief="flat", justify="right"
        )
        self.screen.pack(fill="x", padx=14, pady=12, ipady=8)
        self.screen.focus_set()

    # ---------- KEYPAD ----------
    def build_keypad(self):
        area = tk.Frame(self.root, bg=BG)
        area.pack(fill="both", expand=True, padx=18, pady=8)

        scientific = [
            ("sin", "cos", "tan", "sqrt"),
            ("log", "ln", "pi", "e"),
            ("(", ")", "^", "DEL"),
        ]

        for row_index, row in enumerate(scientific):
            for col_index, label in enumerate(row):
                self.make_button(
                    area, label, row_index, col_index,
                    columns=4, color=KEY
                )

        basic = [
            ("7", "8", "9", "÷"),
            ("4", "5", "6", "×"),
            ("1", "2", "3", "−"),
            ("C", "0", ".", "+"),
            ("DEG/RAD", "x²", "=", "HIST")
        ]

        for row_index, row in enumerate(basic, start=3):
            for col_index, label in enumerate(row):
                color = KEY

                if label in ("÷", "×", "−", "+"):
                    color = BLUE
                elif label == "=":
                    color = GREEN
                elif label == "C":
                    color = RED

                self.make_button(
                    area, label, row_index, col_index,
                    columns=4, color=color
                )

        for col in range(4):
            area.grid_columnconfigure(col, weight=1)

        for row in range(8):
            area.grid_rowconfigure(row, weight=1)

    def make_button(self, parent, label, row, col,
                    columns=4, color=KEY):
        button = tk.Button(
            parent,
            text=label,
            command=lambda: self.press(label),
            bg=color,
            fg=WHITE,
            activebackground="#4B5563",
            activeforeground=WHITE,
            font=("Arial", 12, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2"
        )
        button.grid(
            row=row, column=col,
            sticky="nsew", padx=3, pady=3
        )

    # ---------- HISTORY ----------
    def build_history(self):
        self.history_label = tk.Label(
            self.root,
            text="History: no calculations yet",
            bg=BG, fg=MUTED,
            font=("Arial", 9),
            anchor="w"
        )
        self.history_label.pack(fill="x", padx=20, pady=(0, 10))

    def show_history(self):
        if not self.history:
            message = "History: no calculations yet"
        else:
            message = "History: " + "  |  ".join(self.history[-3:])
        self.history_label.config(text=message)

    # ---------- BUTTON ACTIONS ----------
    def toggle_mode(self):
        self.degrees = not self.degrees
        self.mode_btn.config(
            text="DEG" if self.degrees else "RAD"
        )

    def press(self, key):
        current = self.expression.get()

        if key == "C":
            self.expression.set("")
            return

        if key == "DEL":
            self.expression.set(current[:-1])
            return

        if key == "HIST":
            self.show_history()
            return

        if key == "DEG/RAD":
            self.toggle_mode()
            return

        if key == "=":
            try:
                result = self.calculate(current)
                formatted = f"{result:.10g}"
                self.history.append(f"{current} = {formatted}")
                self.expression.set(formatted)
                self.show_history()
            except Exception:
                self.expression.set("Error")
            return

        functions = {
            "sin": "sin(",
            "cos": "cos(",
            "tan": "tan(",
            "sqrt": "sqrt(",
            "log": "log10(",
            "ln": "ln(",
            "pi": "pi",
            "e": "e",
            "x²": "**2",
            "÷": "/",
            "×": "*",
            "−": "-",
            "^": "**"
        }

        if current == "Error":
            current = ""

        self.expression.set(current + functions.get(key, key))

    # ---------- SAFE MATH EVALUATION ----------
    def calculate(self, expression):
        expression = expression.strip()
        if not expression:
            raise ValueError("Empty expression")

        def trig(fn):
            return (
                lambda x: fn(math.radians(x))
                if self.degrees else fn(x)
            )

        funcs = {
            "sin": trig(math.sin),
            "cos": trig(math.cos),
            "tan": trig(math.tan),
            "sqrt": math.sqrt,
            "log10": math.log10,
            "ln": math.log,
            "pi": math.pi,
            "e": math.e
        }

        ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow
        }

        def visit(node):
            if isinstance(node, ast.Expression):
                return visit(node.body)

            if isinstance(node, ast.Constant):
                if type(node.value) in (int, float):
                    return node.value
                raise ValueError("Invalid number")

            if isinstance(node, ast.Name):
                if node.id in funcs:
                    return funcs[node.id]
                raise ValueError("Unknown name")

            if isinstance(node, ast.UnaryOp):
                x = visit(node.operand)
                if isinstance(node.op, ast.USub):
                    return -x
                if isinstance(node.op, ast.UAdd):
                    return x
                raise ValueError("Invalid operator")

            if isinstance(node, ast.BinOp):
                op = ops.get(type(node.op))
                if op is None:
                    raise ValueError("Invalid operator")
                return op(visit(node.left), visit(node.right))

            if isinstance(node, ast.Call):
                if not isinstance(node.func, ast.Name):
                    raise ValueError("Invalid function")
                fn = funcs.get(node.func.id)
                if not callable(fn) or node.keywords:
                    raise ValueError("Invalid function")
                return fn(*(visit(a) for a in node.args))

            raise ValueError("Invalid expression")

        tree = ast.parse(expression, mode="eval")
        answer = visit(tree)

        if isinstance(answer, bool) or not isinstance(answer, (int, float)):
            raise ValueError("Invalid result")

        if not math.isfinite(answer):
            raise ValueError("Math error")

        return answer


# ---------- MAIN PROGRAM ----------
if __name__ == "__main__":
    window = tk.Tk()
    app = NexusCalculator(window)
    window.mainloop()
