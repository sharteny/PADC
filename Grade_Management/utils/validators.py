def get_nonempty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  This field cannot be empty.")

def get_float_input(prompt, min_val, max_val):
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if min_val <= value <= max_val:
                return value
            print(f"  Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("  That is not a valid number.")

def get_int_input(prompt, min_val, max_val):
    while True:
        raw = input(prompt).strip()
        if raw.isdigit():
            value = int(raw)
            if min_val <= value <= max_val:
                return value
        print(f"  Please enter a whole number between {min_val} and {max_val}.")