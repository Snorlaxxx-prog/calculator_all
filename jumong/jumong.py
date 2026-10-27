
import tkinter as tk
import math
import ast
import operator

# =============== THEME ===============
BG = "#F3F6FB"
WHITE = "#FFFFFF"
NAVY = "#172554"
BLUE = "#2563EB"
LIGHT_BLUE = "#DBEAFE"
PURPLE = "#E0E7FF"
TEXT = "#1E293B"
MUTED = "#64748B"
RED = "#FEE2E2"
BORDER = "#DCE3EE"


class CalculusCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculus Scientific Calculator")
        self.root.geometry("720x600")
        self.root.minsize(620, 540)
        self.root.configure(bg=BG)

        self.expression = tk.StringVar()
        self.degrees = True
        self.history = []

        self.create_header()
        self.create_display()
        self.create_workspace()
        self.create_history()
        self.root.bind("<Return>", lambda event: self.calculate())
        self.root.bind("<Escape>", lambda event: self.clear())

    # =============== HEADER ===============
    def create_header(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=20, pady=(15, 10))

        tk.Label(
            header,
            text="CALCULUS",
            font=("Arial", 21, "bold"),
            bg=BG, fg=NAVY
        ).pack(side="left")

        tk.Label(
            header,
            text="SCIENTIFIC CALCULATOR",
            font=("Arial", 9),
            bg=BG, fg=MUTED
        ).pack(side="left", padx=12, pady=(8, 0))

        self.mode = tk.Button(
            header,
            text="DEG",
            command=self.toggle_mode,
            bg=PURPLE, fg="#3730A3",
            font=("Arial", 10, "bold"),
            relief="flat", width=7, cursor="hand2"
        )
        self.mode.pack(side="right")

    # =============== DISPLAY ===============
    def create_display(self):
        panel = tk.Frame(
            self.root, bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        panel.pack(fill="x", padx=20, pady=5)

        tk.Label(
            panel, text="EXPRESSION",
            bg=WHITE, fg=MUTED,
            font=("Arial", 9, "bold")
        ).pack(anchor="w", padx=15, pady=(10, 0))

        self.entry = tk.Entry(
            panel,
            textvariable=self.expression,
            font=("Consolas", 24),
            bg=WHITE, fg=NAVY,
            insertbackground=BLUE,
            relief="flat", justify="right"
        )
        self.entry.pack(fill="x", padx=15, pady=10, ipady=8)
        self.entry.focus_set()

        self.result_label = tk.Label(
            panel,
            text="Ready to calculate",
            bg=WHITE, fg=MUTED,
            font=("Arial", 10),
            anchor="e"
        )
        self.result_label.pack(fill="x", padx=15, pady=(0, 10))

    # =============== WORKSPACE ===============
    def create_workspace(self):
        workspace = tk.Frame(self.root, bg=BG)
        workspace.pack(
            fill="both", expand=True,
            padx=20, pady=10
        )

        # Scientific panel on the left
        scientific = tk.Frame(
            workspace, bg=PURPLE, width=110
        )
        scientific.pack(side="left", fill="y", padx=(0, 12))
        scientific.pack_propagate(False)

        tk.Label(
            scientific, text="FUNCTIONS",
            bg=PURPLE, fg="#3730A3",
            font=("Arial", 9, "bold")
        ).pack(pady=(10, 5))

        scientific_keys = [
            ("sin", "sin("),
            ("cos", "cos("),
            ("tan", "tan("),
            ("log", "log10("),
            ("ln", "ln("),
            ("√x", "sqrt("),
            ("x²", "**2"),
            ("π", "pi"),
            ("e", "e")
        ]

        for label, value in scientific_keys:
            tk.Button(
                scientific,
                text=label,
                command=lambda v=value: self.insert(v),
                bg=WHITE, fg="#3730A3",
                activebackground=LIGHT_BLUE,
                relief="flat",
                font=("Arial", 11, "bold"),
                cursor="hand2"
            ).pack(fill="x", padx=8, pady=3, ipady=3)

        # Main keypad
        keypad = tk.Frame(workspace, bg=BG)
        keypad.pack(side="left", fill="both", expand=True)

        rows = [
            [("C", "clear"), ("⌫", "delete"),
             ("(", "("), (")", ")")],
            [("7", "7"), ("8", "8"),
             ("9", "9"), ("÷", "/")],
            [("4", "4"), ("5", "5"),
             ("6", "6"), ("×", "*")],
            [("1", "1"), ("2", "2"),
             ("3", "3"), ("−", "-")],
            [("±", "sign"), ("0", "0"),
             (".", "."), ("+", "+")]
        ]

        for r, row in enumerate(rows):
            keypad.grid_rowconfigure(r, weight=1)

            for c, (label, value) in enumerate(row):
                keypad.grid_columnconfigure(c, weight=1)

                color = WHITE
                foreground = TEXT

                if value == "clear":
                    color, foreground = RED, "#B91C1C"
                elif value in ("/", "*", "-", "+"):
                    color, foreground = LIGHT_BLUE, BLUE

                tk.Button(
                    keypad,
                    text=label,
                    command=lambda v=value: self.key_press(v),
                    bg=color, fg=foreground,
                    activebackground="#E2E8F0",
                    relief="flat",
                    font=("Arial", 15, "bold"),
                    cursor="hand2"
                ).grid(
                    row=r, column=c,
                    sticky="nsew", padx=3, pady=3
                )

        tk.Button(
            keypad,
            text="=  Calculate",
            command=self.calculate,
            bg=BLUE, fg=WHITE,
            activebackground="#1D4ED8",
            relief="flat",
            font=("Arial", 13, "bold"),
            cursor="hand2"
        ).grid(
            row=5, column=0, columnspan=4,
            sticky="nsew", padx=3, pady=5, ipady=5
        )
        keypad.grid_rowconfigure(5, weight=1)

    # =============== HISTORY ===============
    def create_history(self):
        panel = tk.Frame(self.root, bg=WHITE)
        panel.pack(fill="x", padx=20, pady=(0, 15))

        tk.Label(
            panel, text="CALCULATION HISTORY",
            bg=WHITE, fg=MUTED,
            font=("Arial", 9, "bold")
        ).pack(anchor="w", padx=12, pady=(7, 2))

        self.history_label = tk.Label(
            panel,
            text="No calculations yet",
            bg=WHITE, fg=TEXT,
            font=("Consolas", 10),
            anchor="w"
        )
        self.history_label.pack(
            fill="x", padx=12, pady=(0, 8)
        )

    def update_history(self, item):
        self.history.append(item)
        self.history = self.history[-3:]
        self.history_label.config(
            text="\n".join(reversed(self.history))
        )

    # =============== INPUT ===============
    def insert(self, value):
        current = self.expression.get()
        if current == "Error":
            current = ""
        self.expression.set(current + value)
        self.entry.focus_set()

    def key_press(self, value):
        current = self.expression.get()

        if value == "clear":
            self.clear()
        elif value == "delete":
            self.expression.set(current[:-1])
        elif value == "sign":
            if current and current != "Error":
                self.expression.set("-(" + current + ")")
        else:
            if current == "Error":
                current = ""
            self.expression.set(current + value)

        self.entry.focus_set()

    def clear(self):
        self.expression.set("")
        self.result_label.config(
            text="Ready to calculate", fg=MUTED
        )

    def toggle_mode(self):
        self.degrees = not self.degrees
        self.mode.config(
            text="DEG" if self.degrees else "RAD"
        )

    # =============== MATH ENGINE ===============
    def calculate(self):
        source = self.expression.get().strip()

        if not source:
            return

        try:
            result = self.evaluate(source)
            formatted = f"{result:.12g}"

            self.result_label.config(
                text="Result: " + formatted,
                fg="#047857"
            )
            self.update_history(
                f"{source} = {formatted}"
            )
            self.expression.set(formatted)

        except Exception:
            self.result_label.config(
                text="Invalid expression",
                fg="#DC2626"
            )

    def evaluate(self, source):
        functions = {
            "sin": lambda x: math.sin(
                math.radians(x) if self.degrees else x
            ),
            "cos": lambda x: math.cos(
                math.radians(x) if self.degrees else x
            ),
            "tan": lambda x: math.tan(
                math.radians(x) if self.degrees else x
            ),
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

        def walk(node):
            if isinstance(node, ast.Expression):
                return walk(node.body)

            if isinstance(node, ast.Constant):
                if type(node.value) in (int, float):
                    return node.value
                raise ValueError()

            if isinstance(node, ast.Name):
                if node.id in functions:
                    return functions[node.id]
                raise ValueError()

            if isinstance(node, ast.BinOp):
                operation = operations.get(type(node.op))
                if operation is None:
                    raise ValueError()
                return operation(
                    walk(node.left), walk(node.right)
                )

            if isinstance(node, ast.UnaryOp):
                if isinstance(node.op, ast.USub):
                    return -walk(node.operand)
                if isinstance(node.op, ast.UAdd):
                    return walk(node.operand)
                raise ValueError()

            if isinstance(node, ast.Call):
                if not isinstance(node.func, ast.Name):
                    raise ValueError()
                function = functions.get(node.func.id)
                if not callable(function) or node.keywords:
                    raise ValueError()
                return function(
                    *(walk(arg) for arg in node.args)
                )

            raise ValueError()

        result = walk(ast.parse(source, mode="eval"))

        if isinstance(result, bool) or not isinstance(
            result, (int, float)
        ):
            raise ValueError()

        if not math.isfinite(result):
            raise ValueError()

        return result


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculusCalculator(root)
    root.mainloop()
