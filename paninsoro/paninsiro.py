
import tkinter as tk
import math
import ast
import operator

# ===== NOVA NEON THEME =====
BG = "#090D0B"
PANEL = "#101B14"
KEY = "#17221A"
SCI = "#13251A"
GREEN = "#39FF88"
MUTED = "#6B8F79"
BORDER = "#215C38"
OPERATOR = "#14532D"
WHITE = "#D9FFE5"
RED = "#7F1D1D"


class NovaCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("NOVA SCI | Scientific Calculator")
        self.root.geometry("540x700")
        self.root.minsize(470, 620)
        self.root.configure(bg=BG)

        self.expression = tk.StringVar()
        self.degrees = True
        self.history = []

        self.create_header()
        self.create_screen()
        self.create_scientific_panel()
        self.create_keypad()
        self.create_footer()

        self.root.bind("<Return>", lambda e: self.calculate())
        self.root.bind("<Escape>", lambda e: self.clear())

    # ===== HEADER =====
    def create_header(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=18, pady=(15, 10))

        tk.Label(
            header, text="NOVA / SCI",
            font=("Consolas", 21, "bold"),
            bg=BG, fg=GREEN
        ).pack(side="left")

        self.mode_button = tk.Button(
            header, text="DEG",
            command=self.toggle_mode,
            bg=SCI, fg=GREEN,
            activebackground=OPERATOR,
            activeforeground=WHITE,
            font=("Consolas", 10, "bold"),
            relief="flat", width=6
        )
        self.mode_button.pack(side="right")

    # ===== DIGITAL DISPLAY =====
    def create_screen(self):
        screen = tk.Frame(
            self.root, bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        screen.pack(fill="x", padx=18, pady=6)

        tk.Label(
            screen, text="CALCULATION OUTPUT",
            font=("Consolas", 9),
            bg=PANEL, fg=MUTED
        ).pack(anchor="w", padx=12, pady=(10, 0))

        self.display = tk.Entry(
            screen,
            textvariable=self.expression,
            font=("Consolas", 25, "bold"),
            bg=PANEL, fg=GREEN,
            insertbackground=GREEN,
            selectbackground=OPERATOR,
            relief="flat", justify="right"
        )
        self.display.pack(fill="x", padx=12, pady=10, ipady=8)
        self.display.focus_set()

        self.status = tk.Label(
            screen, text="READY_",
            font=("Consolas", 9),
            bg=PANEL, fg=GREEN,
            anchor="e"
        )
        self.status.pack(fill="x", padx=12, pady=(0, 10))

    # ===== SCIENTIFIC TOOLBAR =====
    def create_scientific_panel(self):
        panel = tk.Frame(self.root, bg=BG)
        panel.pack(fill="x", padx=18, pady=8)

        functions = [
            ("sin", "sin("), ("cos", "cos("),
            ("tan", "tan("), ("log", "log10("),
            ("ln", "ln("), ("sqrt", "sqrt("),
            ("x²", "**2"), ("xʸ", "**"),
            ("π", "pi"), ("e", "e")
        ]

        for col in range(5):
            panel.grid_columnconfigure(col, weight=1)

        for index, (label, value) in enumerate(functions):
            button = tk.Button(
                panel,
                text=label,
                command=lambda v=value: self.insert(v),
                bg=SCI, fg=GREEN,
                activebackground=OPERATOR,
                activeforeground=WHITE,
                font=("Consolas", 11, "bold"),
                relief="flat",
                bd=1, cursor="hand2"
            )
            button.grid(
                row=index // 5,
                column=index % 5,
                sticky="nsew",
                padx=3, pady=3, ipady=7
            )

    # ===== MAIN KEYPAD =====
    def create_keypad(self):
        panel = tk.Frame(self.root, bg=BG)
        panel.pack(fill="both", expand=True, padx=18, pady=8)

        buttons = [
            [("AC", "clear"), ("DEL", "delete"),
             ("(", "("), (")", ")")],
            [("7", "7"), ("8", "8"),
             ("9", "9"), ("÷", "/")],
            [("4", "4"), ("5", "5"),
             ("6", "6"), ("×", "*")],
            [("1", "1"), ("2", "2"),
             ("3", "3"), ("−", "-")],
            [("0", "0"), (".", "."),
             ("=", "equals"), ("+", "+")]
        ]

        for r, row in enumerate(buttons):
            panel.grid_rowconfigure(r, weight=1)

            for c, (label, action) in enumerate(row):
                panel.grid_columnconfigure(c, weight=1)

                color = KEY
                foreground = WHITE

                if action in ("+", "-", "*", "/"):
                    color = OPERATOR
                    foreground = GREEN
                elif action == "clear":
                    color = RED
                elif action == "equals":
                    color = "#166534"
                    foreground = GREEN

                tk.Button(
                    panel,
                    text=label,
                    command=lambda a=action: self.key_press(a),
                    bg=color, fg=foreground,
                    activebackground=BORDER,
                    activeforeground=GREEN,
                    font=("Consolas", 15, "bold"),
                    relief="flat",
                    bd=1,
                    cursor="hand2"
                ).grid(
                    row=r, column=c,
                    sticky="nsew", padx=4, pady=4
                )

    # ===== FOOTER / HISTORY =====
    def create_footer(self):
        footer = tk.Frame(self.root, bg=BG)
        footer.pack(fill="x", padx=18, pady=(0, 12))

        self.history_label = tk.Label(
            footer,
            text="HISTORY: No calculations",
            bg=BG, fg=MUTED,
            font=("Consolas", 9),
            anchor="w"
        )
        self.history_label.pack(side="left", fill="x", expand=True)

        tk.Button(
            footer, text="CLR HISTORY",
            command=self.clear_history,
            bg=BG, fg=GREEN,
            activebackground=SCI,
            font=("Consolas", 8),
            relief="flat"
        ).pack(side="right")

    # ===== INPUT HANDLING =====
    def insert(self, value):
        current = self.expression.get()

        if current == "Error":
            current = ""

        self.expression.set(current + value)
        self.display.focus_set()

    def key_press(self, action):
        current = self.expression.get()

        if action == "clear":
            self.clear()
        elif action == "delete":
            self.expression.set(current[:-1])
        elif action == "equals":
            self.calculate()
        else:
            if current == "Error":
                current = ""
            self.expression.set(current + action)

        self.display.focus_set()

    def clear(self):
        self.expression.set("")
        self.status.config(text="READY_", fg=GREEN)

    def toggle_mode(self):
        self.degrees = not self.degrees
        self.mode_button.config(
            text="DEG" if self.degrees else "RAD"
        )
        self.status.config(
            text="MODE: DEG" if self.degrees else "MODE: RAD"
        )

    def clear_history(self):
        self.history.clear()
        self.history_label.config(text="HISTORY: No calculations")

    # ===== SAFE EXPRESSION ENGINE =====
    def calculate(self):
        source = self.expression.get().strip()

        if not source:
            return

        try:
            result = self.evaluate(source)
            answer = f"{result:.10g}"

            self.status.config(
                text="RESULT: " + answer, fg=GREEN
            )
            self.history.append(f"{source} = {answer}")
            self.history = self.history[-3:]

            self.history_label.config(
                text="HISTORY: " + " | ".join(self.history)
            )
            self.expression.set(answer)

        except Exception:
            self.status.config(
                text="ERROR: INVALID EXPRESSION", fg="#FF6464"
            )

    def evaluate(self, source):
        def trig(function):
            return lambda x: function(
                math.radians(x) if self.degrees else x
            )

        funcs = {
            "sin": trig(math.sin),
            "cos": trig(math.cos),
            "tan": trig(math.tan),
            "sqrt": math.sqrt,
            "log10": math.log10,
            "ln": math.log,
            "pi": math.pi,
            "e": math.e,
        }

        operations = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
        }

        def visit(node):
            if isinstance(node, ast.Expression):
                return visit(node.body)

            if isinstance(node, ast.Constant):
                if type(node.value) in (int, float):
                    return node.value
                raise ValueError()

            if isinstance(node, ast.Name):
                if node.id in funcs:
                    return funcs[node.id]
                raise ValueError()

            if isinstance(node, ast.UnaryOp):
                if isinstance(node.op, ast.USub):
                    return -visit(node.operand)
                if isinstance(node.op, ast.UAdd):
                    return visit(node.operand)
                raise ValueError()

            if isinstance(node, ast.BinOp):
                operation = operations.get(type(node.op))
                if operation is None:
                    raise ValueError()
                return operation(
                    visit(node.left), visit(node.right)
                )

            if isinstance(node, ast.Call):
                if not isinstance(node.func, ast.Name):
                    raise ValueError()

                function = funcs.get(node.func.id)
                if not callable(function) or node.keywords:
                    raise ValueError()

                return function(
                    *(visit(arg) for arg in node.args)
                )

            raise ValueError("Unsupported expression")

        result = visit(ast.parse(source, mode="eval"))

        if isinstance(result, bool) or not isinstance(
            result, (int, float)
        ):
            raise ValueError()

        if not math.isfinite(result):
            raise ValueError()

        return result


# ===== START APPLICATION =====
if __name__ == "__main__":
    root = tk.Tk()
    calculator = NovaCalculator(root)
    root.mainloop()
