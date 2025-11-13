import funcs
from customtkinter import *

def create_ui():
    global file_entry
    app = CTk()
    app.title('Auto Pyinstaller')
    app.geometry('800x600')

    text_label = CTkLabel(app, text='Add file:', font=('', 18))
    text_label.pack(pady=10)

    file_entry = CTkEntry(app, width=600)
    file_entry.pack(pady=10)

    btn_add = CTkButton(app, text='Add file', command=funcs.add_file)
    btn_add.pack(pady=10)

    app.mainloop()
