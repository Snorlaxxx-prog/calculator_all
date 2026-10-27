
import tkinter as tk
import math

# Main window
root = tk.Tk()
root.title("Red Scientific Calculator")
root.geometry("430x620")
root.resizable(False, False)
root.configure(bg="#240000")

# Theme colors
BG = "#240000"
DISPLAY_BG = "#390000"
RED = "#B30000"
RED_HOVER = "#E00000"
DARK_RED = "#600000"
WHITE = "#FFFFFF"

expression = ""

# Display
display = tk.Entry(
    root,
    font=("Arial", 25, "bold"),
    bg=DISPLAY_BG,
    fg="#FF4D4D",
    insertbackground=WHITE,
    justify="right",
    bd=0
)
display.pack(fill="x", padx=15, pady=20, ipady=18)


def press(value):
    display.insert(tk.END, value)


def clear():
    display.delete(0, tk.END)


def backspace():
    current = display.get()
    display.delete(0, tk.END)
    display.insert(0, current[:-1])


def calculate():
    try:
        expr = display.get()

        # Safe math environment
        allowed = {
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "sqrt": math.sqrt,
            "log": math.log10,
            "ln": math.log,
            "pi": math.pi,
            "e": math.e,
            "abs": abs,
            "factorial": math.factorial,
            "exp": math.exp,
        }

        result = eval(expr, {"__builtins__": {}}, allowed)

        if isinstance(result, float):
            result = round(result, 10)

        clear()
        display.insert(0, str(result))

    except Exception:
        clear()
        display.insert(0, "Math Error")


def add_button(text, row, col, command,
               bg=RED, colspan=1):
    btn = tk.Button(
        buttons_frame,
        text=text,
        font=("Arial", 13, "bold"),
        bg=bg,
        fg=WHITE,
        activebackground=RED_HOVER,
        activeforeground=WHITE,
        bd=0,
        cursor="hand2",
        command=command
    )
    btn.grid(
        row=row,
        column=col,
        columnspan=colspan,
        sticky="nsew",
        padx=4,
        pady=4,
        ipady=10
    )


# Button layout
buttons_frame = tk.Frame(root, bg=BG)
buttons_frame.pack(fill="both", expand=True, padx=10, pady=5)

for col in range(5):
    buttons_frame.columnconfigure(col, weight=1)

for row in range(6):
    buttons_frame.rowconfigure(row, weight=1)

buttons = [
    ("sin(", 0, 0), ("cos(", 0, 1),
    ("tan(", 0, 2), ("sqrt(", 0, 3),
    ("C", 0, 4),

    ("log(", 1, 0), ("ln(", 1, 1),
    ("pi", 1, 2), ("e", 1, 3),
    ("DEL", 1, 4),

    ("(", 2, 0), (")", 2, 1),
    ("**", 2, 2), ("%", 2, 3),
    ("/", 2, 4),

    ("7", 3, 0), ("8", 3, 1),
    ("9", 3, 2), ("*", 3, 3),
    ("-", 3, 4),

    ("4", 4, 0), ("5", 4, 1),
    ("6", 4, 2), ("+", 4, 3),
    (".", 4, 4),

    ("1", 5, 0), ("2", 5, 1),
    ("3", 5, 2), ("0", 5, 3),
    ("=", 5, 4),
]

for text, row, col in buttons:
    if text == "C":
        add_button(text, row, col, clear, DARK_RED)
    elif text == "DEL":
        add_button(text, row, col, backspace, DARK_RED)
    elif text == "=":
        add_button(text, row, col, calculate, "#FF2020")
    else:
        add_button(
            text, row, col,
            lambda t=text: press(t)
        )

# Keyboard support
root.bind("<Return>", lambda event: calculate())
root.bind("<Escape>", lambda event: clear())

root.mainloop()
