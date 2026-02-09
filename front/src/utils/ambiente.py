import platform

def is_linux():
    return platform.system().lower() == "linux"

def is_windows():
    return platform.system().lower() == "windows"
