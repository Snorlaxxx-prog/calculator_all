
import tkinter as tk
import math
import ast
import operator

# ===== ORBIT COLOR PALETTE =====
BG = "#171329"
PANEL = "#241D3C"
KEY = "#29233F"
SCI = "#35284F"
PURPLE = "#8B5CF6"
OPERATOR = "#51408A"
WHITE = "#FFFFFF"
MUTED = "#A7A0C5"
PINK = "#713B66"


class OrbitCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("ORBIT Scientific Suite")
        self.root.geometry("760x660")
        self.root.minsize(650, 580)
        self.root.configure(bg=BG)

        self.expression = tk.StringVar()
        self.degrees = True
        self.history = []

        self.create_navigation()
        self.create_display()
        self.create_main_area()
        self.create_history()

        self.root.bind("<Return>", lambda event: self.calculate())
        self.root.bind("<Escape>", lambda event: self.clear())

    # ===== TOP NAVIGATION =====
    def create_navigation(self):
        nav = tk.Frame(self.root, bg=BG)
        nav.pack(fill="x", padx=20, pady=(15, 12))

        logo = tk.Frame(nav, bg=BG)
        logo.pack(side="left")

        tk.Label(
            logo, text="◈",
            font=("Arial", 26, "bold"),
            bg=BG, fg=PURPLE
        ).pack(side="left", padx=(0, 8))

        tk.Label(
            logo, text="ORBIT",
            font=("Arial", 19, "bold"),
            bg=BG, fg=WHITE
        ).pack(anchor="w")

        tk.Label(
            logo, text="SCIENTIFIC SUITE",
            font=("Arial", 8),
            bg=BG, fg=MUTED
        ).pack(anchor="w")

        self.mode_button = tk.Button(
            nav, text="DEG",
            command=self.toggle_mode,
            bg=SCI, fg="#C4B5FD",
            activebackground=OPERATOR,
            activeforeground=WHITE,
            font=("Arial", 10, "bold"),
            relief="flat", width=8, cursor="hand2"
        )
        self.mode_button.pack(side="right", pady=6)

    # ===== OUTPUT DISPLAY =====
    def create_display(self):
        panel = tk.Frame(self.root, bg=PANEL)
        panel.pack(fill="x", padx=20, pady=5)

        tk.Label(
            panel, text="INPUT EXPRESSION",
            bg=PANEL, fg=MUTED,
            font=("Arial", 9, "bold")
        ).pack(anchor="w", padx=15, pady=(12, 0))

        self.screen = tk.Entry(
            panel,
            textvariable=self.expression,
            font=("Consolas", 26),
            bg=PANEL, fg=WHITE,
            insertbackground=PURPLE,
            relief="flat", justify="right"
        )
        self.screen.pack(fill="x", padx=15, pady=12, ipady=7)
        self.screen.focus_set()

        self.result = tk.Label(
            panel, text="READY TO CALCULATE",
            bg=PANEL, fg="#C4B5FD",
            font=("Arial", 9),
            anchor="e"
        )
        self.result.pack(fill="x", padx=15, pady=(0, 12))

    # ===== TWO-PANEL LAYOUT =====
    def create_main_area(self):
        area = tk.Frame(self.root, bg=BG)
        area.pack(fill="both", expand=True, padx=20, pady=10)

        # Left: scientific operations
        science = tk.Frame(area, bg=BG)
        science.pack(side="left", fill="y", padx=(0, 10))

        tk.Label(
            science, text="FUNCTIONS",
            bg=BG, fg=MUTED,
            font=("Arial", 9, "bold")
        ).pack(anchor="w", pady=(0, 5))

        scientific_keys = [
            ("sin", "sin("),
            ("cos", "cos("),
            ("tan", "tan("),
            ("√x", "sqrt("),
            ("log", "log10("),
            ("ln", "ln("),
            ("x²", "**2"),
            ("xʸ", "**"),
            ("π", "pi"),
            ("e", "e")
        ]

        for label, value in scientific_keys:
            tk.Button(
                science, text=label,
                command=lambda v=value: self.insert(v),
                bg=SCI, fg="#DDD6FE",
                activebackground=OPERATOR,
                activeforeground=WHITE,
                font=("Arial", 11, "bold"),
                relief="flat", width=7,
                cursor="hand2"
            ).pack(fill="x", pady=3, ipady=4)

        # Right: numerical keypad
        keypad = tk.Frame(area, bg=BG)
        keypad.pack(side="left", fill="both", expand=True)

        rows = [
            [("AC", "clear"), ("(", "("),
             (")", ")"), ("÷", "/")],
            [("7", "7"), ("8", "8"),
             ("9", "9"), ("×", "*")],
            [("4", "4"), ("5", "5"),
             ("6", "6"), ("−", "-")],
            [("1", "1"), ("2", "2"),
             ("3", "3"), ("+", "+")],
            [("0", "0"), (".", "."),
             ("DEL", "delete"), ("=", "equals")]
        ]

        for r, row in enumerate(rows):
            keypad.grid_rowconfigure(r, weight=1)

            for c, (label, action) in enumerate(row):
                keypad.grid_columnconfigure(c, weight=1)

                color = KEY
                foreground = WHITE

                if action == "clear":
                    color, foreground = PINK, WHITE
                elif action in ("/", "*", "-", "+"):
                    color, foreground = OPERATOR, WHITE
                elif action == "equals":
                    color, foreground = PURPLE, WHITE

                tk.Button(
                    keypad,
                    text=label,
                    command=lambda a=action: self.press(a),
                    bg=color, fg=foreground,
                    activebackground="#6D52A8",
                    activeforeground=WHITE,
                    font=("Arial", 14, "bold"),
                    relief="flat", bd=0,
                    cursor="hand2"
                ).grid(
                    row=r, column=c,
                    sticky="nsew", padx=4, pady=4
                )

    # ===== HISTORY PANEL =====
    def create_history(self):
        panel = tk.Frame(self.root, bg=PANEL)
        panel.pack(fill="x", padx=20, pady=(0, 15))

        header = tk.Frame(panel, bg=PANEL)
        header.pack(fill="x", padx=12, pady=(8, 3))

        tk.Label(
            header, text="RECENT CALCULATIONS",
            bg=PANEL, fg="#C4B5FD",
            font=("Arial", 9, "bold")
        ).pack(side="left")

        tk.Button(
            header, text="CLEAR",
            command=self.clear_history,
            bg=PANEL, fg=MUTED,
            activebackground=SCI,
            relief="flat", font=("Arial", 8)
        ).pack(side="right")

        self.history_box = tk.Listbox(
            panel, height=3,
            bg=PANEL, fg=WHITE,
            selectbackground=OPERATOR,
            font=("Consolas", 10),
            relief="flat", bd=0,
            highlightthickness=0
        )
        self.history_box.pack(
            fill="x", padx=12, pady=(0, 10)
        )
        self.history_box.bind(
            "<Double-Button-1>", self.reuse_history
        )

    # ===== INTERACTION =====
    def insert(self, value):
        current = self.expression.get()
        if current == "Error":
            current = ""
        self.expression.set(current + value)
        self.screen.focus_set()

    def press(self, action):
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

        self.screen.focus_set()

    def clear(self):
        self.expression.set("")
        self.result.config(
            text="READY TO CALCULATE", fg="#C4B5FD"
        )

    def toggle_mode(self):
        self.degrees = not self.degrees
        self.mode_button.config(
            text="DEG" if self.degrees else "RAD"
        )

    def clear_history(self):
        self.history.clear()
        self.history_box.delete(0, tk.END)

    def reuse_history(self, event=None):
        selection = self.history_box.curselection()
        if selection:
            item = self.history[selection[0]]
            expression = item.split(" = ", 1)[0]
            self.expression.set(expression)

    # ===== SAFE MATH ENGINE =====
    def evaluate(self, source):
        def trig(fn):
            return lambda x: fn(
                math.radians(x) if self.degrees else x
            )

        functions = {
            "sin": trig(math.sin),
            "cos": trig(math.cos),
            "tan": trig(math.tan),
            "sqrt": math.sqrt,
            "log10": math.log10,
            "ln": math.log,
            "pi": math.pi,
            "e": math.e
        }

        operations = {
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
                if node.id in functions:
                    return functions[node.id]
                raise ValueError("Unknown name")

            if isinstance(node, ast.UnaryOp):
                if isinstance(node.op, ast.USub):
                    return -visit(node.operand)
                if isinstance(node.op, ast.UAdd):
                    return visit(node.operand)
                raise ValueError("Invalid operator")

            if isinstance(node, ast.BinOp):
                operation = operations.get(type(node.op))
                if operation is None:
                    raise ValueError("Invalid operator")
                return operation(
                    visit(node.left), visit(node.right)
                )

            if isinstance(node, ast.Call):
                if not isinstance(node.func, ast.Name):
                    raise ValueError("Invalid function")
                function = functions.get(node.func.id)
                if not callable(function) or node.keywords:
                    raise ValueError("Invalid function")
                return function(
                    *(visit(arg) for arg in node.args)
                )

            raise ValueError("Invalid expression")

        answer = visit(ast.parse(source, mode="eval"))

        if isinstance(answer, bool) or not isinstance(
            answer, (int, float)
        ):
            raise ValueError("Invalid result")

        if not math.isfinite(answer):
            raise ValueError("Result out of range")

        return answer

    def calculate(self):
        source = self.expression.get().strip()
        if not source:
            return

        try:
            answer = self.evaluate(source)
            formatted = f"{answer:.12g}"

            self.result.config(
                text="RESULT  =  " + formatted,
                fg="#86EFAC"
            )

            item = f"{source} = {formatted}"
            self.history.insert(0, item)
            self.history = self.history[:30]

            self.history_box.delete(0, tk.END)
            for record in self.history:
                self.history_box.insert(tk.END, record)

            self.expression.set(formatted)

        except Exception:
            self.result.config(
                text="ERROR: CHECK YOUR EXPRESSION",
                fg="#FCA5A5"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = OrbitCalculator(root)
    root.mainloop()
