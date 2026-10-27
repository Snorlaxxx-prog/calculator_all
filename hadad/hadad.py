
import tkinter as tk
import math

root = tk.Tk()
root.title("Hadad Scientific Calculator")
root.geometry("480x620")
root.configure(bg="#ded8c8")
root.resizable(False, False)

expression = ""
degree_mode = True

# Colors
BODY = "#ded8c8"
NUMBER = "#f5f0e5"
FUNCTION = "#b8c4cc"
OPERATOR = "#d68b46"
DARK = "#253746"

# Calculator heading
tk.Label(
    root,
    text="SCIENTIFIC ",
    font=("Arial", 13, "bold"),
    bg=BODY,
    fg="#343b40"
).pack(pady=(12, 5))

# LCD-style display
display = tk.Entry(
    root,
    font=("Consolas", 22),
    bg=DARK,
    fg="#c7edb0",
    insertbackground="white",
    justify="right",
    bd=6,
    relief="sunken"
)
display.pack(fill="x", padx=15, pady=10, ipady=12)

mode_label = tk.Label(
    root,
    text="ANGLE: DEG",
    font=("Arial", 9, "bold"),
    bg=BODY,
    fg="#343b40"
)
mode_label.pack(anchor="w", padx=18, pady=(0, 8))


def calculate():
    global expression
    try:
        allowed = {
            "sin": lambda x: math.sin(
                math.radians(x) if degree_mode else x
            ),
            "cos": lambda x: math.cos(
                math.radians(x) if degree_mode else x
            ),
            "tan": lambda x: math.tan(
                math.radians(x) if degree_mode else x
            ),
            "sqrt": math.sqrt,
            "log": math.log10,
            "ln": math.log,
            "pi": math.pi,
            "e": math.e,
            "abs": abs,
            "factorial": math.factorial
        }

        result = eval(expression, {"__builtins__": {}}, allowed)

        if isinstance(result, float):
            expression = format(result, ".12g")
        else:
            expression = str(result)

        display.delete(0, tk.END)
        display.insert(0, expression)

    except Exception:
        display.delete(0, tk.END)
        display.insert(0, "Math Error")
        expression = ""


def press(key):
    global expression, degree_mode

    if key == "AC":
        expression = ""
        display.delete(0, tk.END)

    elif key == "DEL":
        expression = expression[:-1]
        display.delete(0, tk.END)
        display.insert(0, expression)

    elif key == "=":
        calculate()

    elif key == "DEG/RAD":
        degree_mode = not degree_mode
        mode_label.config(
            text="ANGLE: DEG" if degree_mode else "ANGLE: RAD"
        )

    elif key == "x²":
        expression += "**2"
        display.delete(0, tk.END)
        display.insert(0, expression)

    elif key == "√":
        expression += "sqrt("
        display.delete(0, tk.END)
        display.insert(0, expression)

    elif key == "π":
        expression += "pi"
        display.delete(0, tk.END)
        display.insert(0, expression)

    elif key == "×":
        expression += "*"
        display.delete(0, tk.END)
        display.insert(0, expression)

    elif key == "÷":
        expression += "/"
        display.delete(0, tk.END)
        display.insert(0, expression)

    elif key == "−":
        expression += "-"
        display.delete(0, tk.END)
        display.insert(0, expression)

    else:
        expression += key
        display.delete(0, tk.END)
        display.insert(0, expression)


# Scientific function panel
functions = [
    ["sin(", "cos(", "tan(", "log(", "ln("],
    ["√", "x²", "x**", "(", ")"],
    ["π", "e", "factorial(", "DEG/RAD", "AC"]
]

panel = tk.Frame(root, bg=BODY)
panel.pack(fill="x", padx=12, pady=3)

for r, row in enumerate(functions):
    for c, key in enumerate(row):
        color = OPERATOR if key in ("AC", "DEG/RAD") else FUNCTION

        tk.Button(
            panel,
            text=key,
            font=("Arial", 11, "bold"),
            bg=color,
            fg="#202a30",
            relief="raised",
            bd=3,
            command=lambda k=key: press(k)
        ).grid(
            row=r, column=c,
            sticky="nsew", padx=3, pady=3, ipady=7
        )

for c in range(5):
    panel.columnconfigure(c, weight=1)

# Separate numeric keypad
keypad = [
    ["7", "8", "9", "÷"],
    ["4", "5", "6", "×"],
    ["1", "2", "3", "−"],
    ["0", ".", "DEL", "+"],
    ["=", "=", "=", "="]
]

numbers = tk.Frame(root, bg=BODY)
numbers.pack(fill="both", expand=True, padx=12, pady=6)

for r, row in enumerate(keypad):
    for c, key in enumerate(row):
        if r == 4:
            if c == 0:
                btn = tk.Button(
                    numbers,
                    text="CALCULATE",
                    font=("Arial", 12, "bold"),
                    bg=OPERATOR,
                    fg="white",
                    relief="raised",
                    bd=4,
                    command=lambda: press("=")
                )
                btn.grid(
                    row=r, column=0, columnspan=4,
                    sticky="nsew", padx=3, pady=3, ipady=7
                )
            break

        color = OPERATOR if key in ["÷", "×", "−", "+", "DEL"] else NUMBER

        tk.Button(
            numbers,
            text=key,
            font=("Arial", 15, "bold"),
            bg=color,
            fg="#202a30",
            relief="raised",
            bd=3,
            command=lambda k=key: press(k)
        ).grid(
            row=r, column=c,
            sticky="nsew", padx=3, pady=3, ipady=9
        )

for r in range(5):
    numbers.rowconfigure(r, weight=1)

for c in range(4):
    numbers.columnconfigure(c, weight=1)

root.mainloop()
