
import tkinter as tk
import math
import ast
import operator

# Scientific Calculator using Tkinter

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("440x570")
        self.root.resizable(False, False)
        self.root.configure(bg="#20252b")

        self.expression = tk.StringVar(value="")
        self.degrees = True

        # Display
        display = tk.Entry(
            root,
            textvariable=self.expression,
            font=("Arial", 24),
            justify="right",
            bg="#303841",
            fg="white",
            insertbackground="white",
            bd=10
        )
        display.pack(fill="x", padx=12, pady=15, ipady=12)

        # Degree / Radian toggle
        self.mode_button = tk.Button(
            root,
            text="Mode: DEG",
            command=self.toggle_mode,
            font=("Arial", 11, "bold"),
            bg="#00a8a8",
            fg="white"
        )
        self.mode_button.pack(fill="x", padx=12, pady=3)

        # Calculator buttons
        buttons = [
            ["sin", "cos", "tan", "sqrt", "C"],
            ["asin", "acos", "atan", "x²", "DEL"],
            ["log", "ln", "(", ")", "÷"],
            ["7", "8", "9", "π", "×"],
            ["4", "5", "6", "e", "−"],
            ["1", "2", "3", "!", "+"],
            ["±", "0", ".", "^", "="]
        ]

        frame = tk.Frame(root, bg="#20252b")
        frame.pack(fill="both", expand=True, padx=10, pady=8)

        for r, row in enumerate(buttons):
            frame.grid_rowconfigure(r, weight=1)
            for c, text in enumerate(row):
                frame.grid_columnconfigure(c, weight=1)

                color = "#37424e"
                if text == "=":
                    color = "#00a86b"
                elif text in ("C", "DEL"):
                    color = "#c0392b"
                elif text in ("+", "−", "×", "÷", "^"):
                    color = "#1769aa"

                btn = tk.Button(
                    frame,
                    text=text,
                    font=("Arial", 13, "bold"),
                    bg=color,
                    fg="white",
                    activebackground="#596674",
                    activeforeground="white",
                    bd=0,
                    command=lambda value=text: self.press(value)
                )
                btn.grid(
                    row=r, column=c,
                    sticky="nsew",
                    padx=3, pady=3
                )

    def toggle_mode(self):
        self.degrees = not self.degrees
        mode = "DEG" if self.degrees else "RAD"
        self.mode_button.config(text=f"Mode: {mode}")

    def press(self, value):
        current = self.expression.get()

        if value == "C":
            self.expression.set("")
            return

        if value == "DEL":
            self.expression.set(current[:-1])
            return

        if value == "=":
            try:
                result = self.calculate(current)
                self.expression.set(str(result))
            except Exception:
                self.expression.set("Error")
            return

        if value == "±":
            if current and current != "Error":
                try:
                    result = self.calculate(current)
                    self.expression.set(str(-result))
                except Exception:
                    self.expression.set("-(" + current + ")")
            return

        replacements = {
            "×": "*",
            "÷": "/",
            "−": "-",
            "^": "**",
            "π": "pi",
            "x²": "**2",
            "!": "!",
            "sin": "sin(",
            "cos": "cos(",
            "tan": "tan(",
            "asin": "asin(",
            "acos": "acos(",
            "atan": "atan(",
            "sqrt": "sqrt(",
            "log": "log10(",
            "ln": "log(",
            "e": "e"
        }

        addition = replacements.get(value, value)

        if value == "x²":
            addition = "**2"

        if current == "Error":
            current = ""

        self.expression.set(current + addition)

    def calculate(self, expression):
        expression = expression.strip()

        if not expression:
            return 0

        # Support factorial notation, e.g. 5!
        expression = self.replace_factorials(expression)

        # Only explicitly allowed mathematical functions and constants
        def trig(function):
            if self.degrees:
                return lambda x: function(math.radians(x))
            return function

        def inverse_trig(function):
            if self.degrees:
                return lambda x: math.degrees(function(x))
            return function

        allowed = {
            "sin": trig(math.sin),
            "cos": trig(math.cos),
            "tan": trig(math.tan),
            "asin": inverse_trig(math.asin),
            "acos": inverse_trig(math.acos),
            "atan": inverse_trig(math.atan),
            "sqrt": math.sqrt,
            "log": math.log,
            "log10": math.log10,
            "pi": math.pi,
            "e": math.e,
            "abs": abs
        }

        # Parse the expression and permit only safe arithmetic
        tree = ast.parse(expression, mode="eval")

        def evaluate(node):
            if isinstance(node, ast.Expression):
                return evaluate(node.body)

            if isinstance(node, ast.Constant):
                if type(node.value) in (int, float):
                    return node.value
                raise ValueError("Invalid number")

            if isinstance(node, ast.BinOp):
                operations = {
                    ast.Add: operator.add,
                    ast.Sub: operator.sub,
                    ast.Mult: operator.mul,
                    ast.Div: operator.truediv,
                    ast.Pow: operator.pow,
                    ast.Mod: operator.mod
                }
                operation = operations.get(type(node.op))
                if operation is None:
                    raise ValueError("Invalid operation")
                return operation(
                    evaluate(node.left),
                    evaluate(node.right)
                )

            if isinstance(node, ast.UnaryOp):
                if isinstance(node.op, ast.USub):
                    return -evaluate(node.operand)
                if isinstance(node.op, ast.UAdd):
                    return evaluate(node.operand)
                raise ValueError("Invalid sign")

            if isinstance(node, ast.Name):
                if node.id in allowed:
                    return allowed[node.id]
                raise ValueError("Unknown name")

            if isinstance(node, ast.Call):
                if not isinstance(node.func, ast.Name):
                    raise ValueError("Invalid function")
                function = allowed.get(node.func.id)
                if not callable(function) or node.keywords:
                    raise ValueError("Invalid function")
                args = [evaluate(arg) for arg in node.args]
                return function(*args)

            raise ValueError("Invalid expression")

        result = evaluate(tree)

        if isinstance(result, bool) or not isinstance(result, (int, float)):
            raise ValueError("Invalid result")

        if not math.isfinite(result):
            raise ValueError("Result is not finite")

        return result

    def replace_factorials(self, expression):
        # Convert n! to factorial(n), without changing !=
        result = ""
        i = 0

        while i < len(expression):
            if expression[i] == "!":
                j = len(result) - 1

                if j < 0:
                    raise ValueError("Invalid factorial")

                if result[j] == ")":
                    depth = 1
                    j -= 1
                    while j >= 0 and depth:
                        if result[j] == ")":
                            depth += 1
                        elif result[j] == "(":
                            depth -= 1
                        j -= 1
                    start = j + 1
                else:
                    while j >= 0 and (
                        result[j].isalnum() or result[j] == "."
                    ):
                        j -= 1
                    start = j + 1

                operand = result[start:]
                if not operand:
                    raise ValueError("Invalid factorial")

                result = result[:start] + "factorial(" + operand + ")"
            else:
                result += expression[i]

            i += 1

        return result


# Run the calculator
if __name__ == "__main__":
    root = tk.Tk()
    calculator = ScientificCalculator(root)
    root.mainloop()
