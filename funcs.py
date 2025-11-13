import ui
from tkinter import filedialog
from customtkinter import CTk, CTkLabel, CTkButton

def add_file():
    fp = filedialog.askopenfilename(
        filetypes=[("Python files", "*.py"), ("Все файлы", "*.*")]
    )
    if fp:
        ui.file_entry.delete(0, "end")
        ui.file_entry.insert(0, fp) 