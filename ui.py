from customtkinter import *
import funcs

def create_ui():
    app = CTk()
    app.title('Auto Pyinstaller')
    app.geometry('550x350')
    

    ui_refs = {}

    use_noconsole = BooleanVar(value=True)
    use_onefile = BooleanVar(value=True)
    use_onedir = BooleanVar(value=False)
    use_windowed = BooleanVar(value=False)

    ui_refs['use_noconsole'] = use_noconsole
    ui_refs['use_onefile'] = use_onefile
    ui_refs['use_onedir'] = use_onedir
    ui_refs['use_windowed'] = use_windowed

    frame = CTkFrame(app, fg_color="transparent")
    frame.grid(row=0, column=0, padx=10, pady=10)

    CTkLabel(frame, text='Add file:', font=('', 16)).grid(row=0, column=0, columnspan=2, pady=(5, 0))
    file_entry = CTkEntry(frame, width=350)
    file_entry.grid(row=1, column=0, pady=5)
    CTkButton(frame, text='Browse', command=funcs.add_file).grid(row=1, column=1, padx=10, pady=5)

    CTkLabel(frame, text='Save EXE to folder:', font=('', 16)).grid(row=2, column=0, columnspan=2, pady=(15, 0))
    output_entry = CTkEntry(frame, width=350)
    output_entry.grid(row=3, column=0, pady=5)
    CTkButton(frame, text='Select folder', command=funcs.choose_output_folder).grid(row=3, column=1, padx=10, pady=5)

    notification_label = CTkLabel(frame, text='', font=('', 14))
    notification_label.grid(row=8, column=0, columnspan=2, pady=10)

    funcs.set_ui_refs(file_entry, output_entry, notification_label, app)

    CTkButton(frame, text='Start', command=lambda: funcs.start(ui_refs)).grid(row=4, column=0, columnspan=2, pady=10)

    CTkLabel(frame, text='Choose methods').grid(row=5, column=0, columnspan=2, pady=(10, 0))
    options_frame = CTkFrame(frame, fg_color="transparent")
    options_frame.grid(row=6, column=0, columnspan=2, pady=10)
    options_frame.grid_columnconfigure((0,1,2,3), weight=1)

    CTkCheckBox(options_frame, text='No console', variable=use_noconsole).grid(row=0, column=0, padx=5, pady=5)
    CTkCheckBox(options_frame, text='One file', variable=use_onefile).grid(row=0, column=1, padx=5, pady=5)
    CTkCheckBox(options_frame, text='One dir', variable=use_onedir).grid(row=0, column=2, padx=5, pady=5)
    CTkCheckBox(options_frame, text='Windowed', variable=use_windowed).grid(row=0, column=3, padx=5, pady=5)

    app.mainloop()
