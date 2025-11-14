from customtkinter import *
import funcs

def create_ui():
    app = CTk()
    app.title('Auto Pyinstaller')
    app.geometry('510x300')

    ui_refs = {}

    use_noconsole = BooleanVar(value=True)
    use_onefile = BooleanVar(value=True)
    use_onedir = BooleanVar(value=False)
    use_windowed = BooleanVar(value=False)

    ui_refs['use_noconsole'] = use_noconsole
    ui_refs['use_onefile'] = use_onefile
    ui_refs['use_onedir'] = use_onedir
    ui_refs['use_windowed'] = use_windowed

    frame = CTkFrame(app)
    frame.grid(row=0, column=0, padx=10, pady=10)

    text_label = CTkLabel(frame, text='Add file:', font=('', 18))
    text_label.grid(row=0, column=0, columnspan=2, pady=10)

    file_entry = CTkEntry(frame, width=350)
    file_entry.grid(row=1, column=0, pady=10)

    notification_label = CTkLabel(frame, text='', font=('', 14))
    notification_label.grid(row=5, column=0, columnspan=2, pady=10)

    funcs.set_ui_refs(file_entry, notification_label, app)

    btn_add = CTkButton(frame, text='Add file', command=funcs.add_file)
    btn_add.grid(row=1, column=1, padx=10, pady=10)

    btn_start = CTkButton(frame, text='Start', command=lambda: funcs.start(ui_refs))
    btn_start.grid(row=2, column=0, columnspan=2, pady=10)

    text1_label = CTkLabel(frame, text='Choose methods')
    text1_label.grid(row=3, column=0, columnspan=2, pady=10)

    options_frame = CTkFrame(frame)
    options_frame.grid(row=4, column=0, columnspan=2, pady=10)
    options_frame.grid_columnconfigure((0,1,2,3), weight=1)

    CTkCheckBox(options_frame, text='No console', variable=use_noconsole).grid(row=0, column=0, padx=5, pady=5)
    CTkCheckBox(options_frame, text='One file', variable=use_onefile).grid(row=0, column=1, padx=5, pady=5)
    CTkCheckBox(options_frame, text='One dir', variable=use_onedir).grid(row=0, column=2, padx=5, pady=5)
    CTkCheckBox(options_frame, text='Windowed', variable=use_windowed).grid(row=0, column=3, padx=5, pady=5)

    app.mainloop()
