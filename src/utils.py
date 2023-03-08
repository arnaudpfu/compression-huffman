def read_file(path, reading_mode = ""):
    with open(path, "r" + reading_mode) as f:
        content = f.read()
    return content