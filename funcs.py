from tkinter import filedialog, Tk
import subprocess
import os
import shutil

file_entry = None
output_entry = None
notification_label = None
root = None
save_name_entry = None

def set_ui_refs(entry_file, entry_output, label, main_root, entry_name):
    global file_entry, output_entry, notification_label, root, save_name_entry
    file_entry = entry_file
    output_entry = entry_output
    notification_label = label
    root = main_root
    save_name_entry = entry_name
def add_file():
    if not file_entry:
        return
    fp = filedialog.askopenfilename(filetypes=[('Python files', '*.py'), ('Все файлы', '*.*')])
    if fp:
        file_entry.delete(0, 'end')
        file_entry.insert(0, fp)
def choose_output_folder():
    if not output_entry:
        return
    folder = filedialog.askdirectory(title='Select a folder to save .exe')
    if folder:
        output_entry.delete(0, 'end')
        output_entry.insert(0, folder)
def show_notification(message):
    if notification_label and root:
        notification_label.configure(text=message)
        root.after(3000, lambda: notification_label.configure(text=''))
def remove_dir_except_file(path, ignore_filename):
    for root_dir, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if name != ignore_filename:
                os.remove(os.path.join(root_dir, name))
        for name in dirs:
            shutil.rmtree(os.path.join(root_dir, name), ignore_errors=True)
def start_build_process(fp, output_folder, options):
    global save_name_entry
    raw_name = save_name_entry.get().strip() if save_name_entry else ''
    if not raw_name:
        raw_name = os.path.splitext(os.path.basename(fp))[0]
    name = os.path.splitext(raw_name)[0]

    dist_path = os.path.join(os.getcwd(), 'dist')
    build_path = os.path.join(os.getcwd(), 'build')
    spec_file = f'{name}.spec'

    try:
        temp_root = Tk()
        tk_library = temp_root.tk.exprstring('$tcl_library')
        tcl_path = os.path.dirname(tk_library)
        temp_root.destroy()
    except Exception:
        tcl_path = None

    cmd = ['pyinstaller', fp, '--name', name]

    if tcl_path:
        add_data = f'{tcl_path};tk'
        cmd.append(f'--add-data={add_data}')

    if options.get('noconsole'):
        cmd.append('--noconsole')
    if options.get('onefile'):
        cmd.append('--onefile')
    if options.get('onedir'):
        cmd.append('--onedir')
    if options.get('windowed'):
        cmd.append('--windowed')

    try:
        subprocess.run(cmd, check=True)

        exe_path = (
            os.path.join(dist_path, f'{name}.exe')
            if options.get('onefile')
            else os.path.join(dist_path, name, f'{name}.exe')
        )

        if os.path.exists(exe_path):
            os.makedirs(output_folder, exist_ok=True)
            shutil.move(exe_path, os.path.join(output_folder, f'{name}.exe'))

        for path in [dist_path, build_path, '__pycache__']:
            if os.path.exists(path):
                remove_dir_except_file(path, f'{name}.exe')

        if os.path.exists(spec_file):
            os.remove(spec_file)

        show_notification(f'Build complete! File: {name}.exe saved to {output_folder}')

    except subprocess.CalledProcessError:
        show_notification('Assembly error!')
def start(ui_refs):
    if not file_entry:
        return

    fp = file_entry.get()
    if not fp:
        show_notification('Specify file to compile')
        return

    output_folder = output_entry.get() if output_entry else ''
    if not output_folder:
        show_notification('Specify save save')
        return

    options = {
        'noconsole': ui_refs['use_noconsole'].get(),
        'onefile': ui_refs['use_onefile'].get(),
        'onedir': ui_refs['use_onedir'].get(),
        'windowed': ui_refs['use_windowed'].get(),
    }

    start_build_process(fp, output_folder, options)
def add_icon(icon_entry):
    if not icon_entry:
        return
    icon_path = filedialog.askopenfilename(filetypes=[('ICO files', '*.ico'), ('Все файлы', '*.*')])
    if icon_path:
        icon_entry.delete(0, 'end')
        icon_entry.insert(0, icon_path)
    if file_entry:
        file_path = file_entry.get()
        if file_path and os.path.isfile(file_path):
            base, ext = os.path.splitext(file_path)
            if ext.lower() == '.py':
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                icon_line = f"import sys\nsys._MEIPASS = '{os.path.dirname(icon_path)}'\n"
                if icon_line not in lines:
                    lines.insert(0, icon_line)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.writelines(lines)
                show_notification('Icon added to the script.')
    