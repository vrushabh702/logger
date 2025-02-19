from cx_Freeze import setup, Executable

executables = [Executable("keylogger.py")]

setup(
    name="Ethical Keylogger",
    version="1.0",
    description="An ethical keylogger for penetration testing",
    executables=executables
)