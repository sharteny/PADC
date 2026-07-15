def make_bar(current, maximum, length):
    if maximum == 0:
        filled = 0
    else:
        filled = int((current / maximum) * length)
    return "#" * filled + "." * (length - filled)