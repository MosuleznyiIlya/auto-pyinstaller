from tkinter import filedialog
import subprocess

file_entry = None
notification_label = None
root = None

def set_ui_refs(entry, label, main_root):
    global file_entry, notification_label, root
    file_entry = entry
    notification_label = label
    root = main_root

def add_file():
    fp = filedialog.askopenfilename(
        filetypes=[("Python files", "*.py"), ("Все файлы", "*.*")]
    )
    if fp and file_entry:
        file_entry.delete(0, "end")
        file_entry.insert(0, fp)

def show_notification(message):
    if notification_label and root:
        notification_label.configure(text=message)
        root.after(3000, lambda: notification_label.configure(text=""))

def start_build_process(fp, options):
    cmd = ["pyinstaller", fp]
    if options["noconsole"]:
        cmd.append("--noconsole")
    if options["onefile"]:
        cmd.append("--onefile")
    if options["onedir"]:
        cmd.append("--onedir")
    if options["windowed"]:
        cmd.append("--windowed")
    try:
        subprocess.run(cmd, check=True)
        show_notification("Сборка завершена успешно!")
    except subprocess.CalledProcessError:
        show_notification("Ошибка при сборке!")

def start(ui_refs):
    if not file_entry:
        return
    fp = file_entry.get()
    if not fp:
        show_notification("Укажите файл")
        return
    options = {
        "noconsole": ui_refs["use_noconsole"].get(),
        "onefile": ui_refs["use_onefile"].get(),
        "onedir": ui_refs["use_onedir"].get(),
        "windowed": ui_refs["use_windowed"].get(),
    }
    start_build_process(fp, options)
