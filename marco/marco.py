
import tkinter as tk
import math

# Classic Scientific Calculator
root = tk.Tk()
root.title("Scientific Calculator")
root.geometry("440x600")
root.configure(bg="#c8c8c8")
root.resizable(False, False)

expression = ""
degree_mode = True

# Display
display = tk.Entry(
    root,
    font=("Arial", 23),
    bg="#dce6d0",
    fg="#202820",
    justify="right",
    bd=5,
    relief="sunken"
)
display.pack(fill="x", padx=12, pady=15, ipady=12)


def press(value):
    global expression

    if value == "AC":
        expression = ""
        display.delete(0, tk.END)

    elif value == "DEL":
        expression = expression[:-1]
        display.delete(0, tk.END)
        display.insert(0, expression)

    elif value == "=":
        try:
            result = eval(
                expression,
                {"__builtins__": {}},
                {
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
                    "factorial": math.factorial,
                    "abs": abs
                }
            )
            expression = str(result)
            display.delete(0, tk.END)
            display.insert(0, expression)
        except Exception:
            display.delete(0, tk.END)
            display.insert(0, "Math Error")
            expression = ""

    elif value == "DEG/RAD":
        global degree_mode
        degree_mode = not degree_mode
        mode_label.config(
            text="DEG MODE" if degree_mode else "RAD MODE"
        )

    else:
        expression += value
        display.delete(0, tk.END)
        display.insert(0, expression)


# Mode indicator
mode_label = tk.Label(
    root,
    text="DEG MODE",
    font=("Arial", 10, "bold"),
    bg="#c8c8c8",
    fg="#303030"
)
mode_label.pack(anchor="w", padx=16, pady=(0, 8))

# Traditional scientific calculator button layout
buttons = [
    ["sin(", "cos(", "tan(", "log(", "ln("],
    ["sqrt(", "(", ")", "**2", "**"],
    ["pi", "e", "factorial(", "abs(", "DEG/RAD"],
    ["7", "8", "9", "/", "DEL"],
    ["4", "5", "6", "*", "AC"],
    ["1", "2", "3", "-", "="],
    ["0", ".", "+", "**0.5", "="]
]

button_frame = tk.Frame(root, bg="#c8c8c8")
button_frame.pack(fill="both", expand=True, padx=10, pady=5)

for r, row in enumerate(buttons):
    for c, value in enumerate(row):
        # Traditional gray keys and darker function keys
        if value in ["AC", "DEL"]:
            color = "#b86b62"
        elif value in ["=", "DEG/RAD"]:
            color = "#8c9caa"
        elif value in [
            "sin(", "cos(", "tan(", "log(", "ln(",
            "sqrt(", "factorial(", "abs(", "pi", "e"
        ]:
            color = "#b8c0c5"
        else:
            color = "#eeeeee"

        btn = tk.Button(
            button_frame,
            text=value,
            font=("Arial", 12, "bold"),
            bg=color,
            fg="#222222",
            activebackground="#d0d0d0",
            relief="raised",
            bd=3,
            command=lambda v=value: press(v)
        )
        btn.grid(
            row=r,
            column=c,
            sticky="nsew",
            padx=3,
            pady=3,
            ipady=8
        )

for r in range(len(buttons)):
    button_frame.rowconfigure(r, weight=1)

for c in range(5):
    button_frame.columnconfigure(c, weight=1)

root.mainloop()
