from tkinter import filedialog
import subprocess
import os
import shutil

file_entry = None
output_entry = None
notification_label = None
root = None

def set_ui_refs(entry_file, entry_output, label, main_root):
    global file_entry, output_entry, notification_label, root
    file_entry = entry_file
    output_entry = entry_output
    notification_label = label
    root = main_root
def add_file():
    fp = filedialog.askopenfilename(
        filetypes=[('Python files', '*.py'), ('Все файлы', '*.*')]
    )
    if fp and file_entry:
        file_entry.delete(0, 'end')
        file_entry.insert(0, fp)
def choose_output_folder():
    folder = filedialog.askdirectory(title='Выбери папку для сохранения .exe')
    if folder and output_entry:
        output_entry.delete(0, 'end')
        output_entry.insert(0, folder)
def show_notification(message):
    if notification_label and root:
        notification_label.configure(text=message)
        root.after(3000, lambda: notification_label.configure(text=''))
def start_build_process(fp, output_folder, options):
    filename = os.path.basename(fp)
    name = os.path.splitext(filename)[0]

    dist_path = os.path.join(os.getcwd(), 'dist')
    build_path = os.path.join(os.getcwd(), 'build')
    spec_file = f'{name}.spec'

    cmd = ['pyinstaller', fp]

    if options['noconsole']:
        cmd.append('--noconsole')
    if options['onefile']:
        cmd.append('--onefile')
    if options['onedir']:
        cmd.append('--onedir')
    if options['windowed']:
        cmd.append('--windowed')

    try:
        subprocess.run(cmd, check=True)

        exe_path = None
        if options['onefile']:
            exe_path = os.path.join(dist_path, f'{name}.exe')
        else:
            exe_path = os.path.join(dist_path, name, f'{name}.exe')

        if os.path.exists(exe_path):
            os.makedirs(output_folder, exist_ok=True)
            shutil.move(exe_path, os.path.join(output_folder, f'{name}.exe'))
            show_notification('Сборка завершена успешно! .exe сохранён')

        for path in [dist_path, build_path, spec_file, '__pycache__']:
            if os.path.exists(path):
                if os.path.isdir(path):
                    shutil.rmtree(path, ignore_errors=True)
                else:
                    os.remove(path)

    except subprocess.CalledProcessError:
        show_notification('Ошибка при сборке!')
def start(ui_refs):
    if not file_entry:
        return

    fp = file_entry.get()
    if not fp:
        show_notification('Укажи файл')
        return

    output_folder = output_entry.get() if output_entry else ''
    if not output_folder:
        show_notification('Укажи папку сохранения')
        return

    options = {
        'noconsole': ui_refs['use_noconsole'].get(),
        'onefile': ui_refs['use_onefile'].get(),
        'onedir': ui_refs['use_onedir'].get(),
        'windowed': ui_refs['use_windowed'].get(),
    }

    start_build_process(fp, output_folder, options)
