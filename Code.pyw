import os
import shutil
import tkinter as tk
from tkinter import messagebox


def find_combit_folder(input_path: str) -> str | None:
    """Sucht im übergebenen Pfad nach dem Ordner 'combit' und gibt dessen Pfad zurück."""
    # Bereinigt Leerzeichen und Anführungszeichen (falls in Windows 'Als Pfad kopieren' genutzt wurde)
    clean_path = input_path.strip().strip('"').strip("'")
    if not clean_path:
        return None

    # Pfad normalisieren (z. B. / zu \)
    norm_path = os.path.normpath(clean_path)
    parts = norm_path.split(os.sep)

    # Nach 'combit' in den Pfadbestandteilen suchen
    for i, part in enumerate(parts):
        if part.lower() == "combit":
            target = os.sep.join(parts[: i + 1])
            # Sonderfall Laufwerksbuchstabe unter Windows (z.B. C:)
            if len(target) == 2 and target[1] == ":":
                target += os.sep
            return target

    return None


def process_deletion():
    raw_input = entry_path.get()
    combit_dir = find_combit_folder(raw_input)

    if not combit_dir:
        messagebox.showerror(
            "Ungültiger Pfad",
            "Im angegebenen Pfad konnte kein Ordner namens 'combit' gefunden werden.\n"
            "Bitte prüfen Sie die Eingabe.",
        )
        return

    if not os.path.exists(combit_dir):
        messagebox.showwarning(
            "Ordner nicht gefunden",
            f"Der ermittelte Ordner existiert nicht (mehr):\n{combit_dir}",
        )
        return

    if not os.path.isdir(combit_dir):
        messagebox.showerror(
            "Fehler", f"Der gefundene Pfad ist kein Ordner:\n{combit_dir}"
        )
        return

    try:
        # Ordner inklusive aller Unterordner und Dateien löschen
        shutil.rmtree(combit_dir)

        # Positive Rückmeldung; nach Klick auf OK wird das Programm beendet
        messagebox.showinfo(
            "Erfolgreich gelöscht",
            f"Der Ordner und alle darin enthaltenen Dateien wurden erfolgreich gelöscht:\n\n{combit_dir}",
        )
        root.destroy()

    except PermissionError:
        messagebox.showerror(
            "Zugriff verweigert",
            f"Einige Dateien im Ordner werden noch von einem Programm verwendet:\n\n{combit_dir}\n\n"
            "Bitte schließen Sie das entsprechende Programm und versuchen Sie es erneut.",
        )
    except Exception as e:
        messagebox.showerror(
            "Fehler beim Löschen",
            f"Es ist ein unerwarteter Fehler aufgetreten:\n{e}",
        )


# --- GUI Setup ---
root = tk.Tk()
root.title("Combit-Ordner bereinigen")
root.geometry("560x160")
root.resizable(False, False)

# Fenster auf dem Bildschirm zentrieren
root.update_idletasks()
x = (root.winfo_screenwidth() // 2) - (560 // 2)
y = (root.winfo_screenheight() // 2) - (160 // 2)
root.geometry(f"+{x}+{y}")

# Beschriftung
lbl_instruction = tk.Label(
    root, text="Bitte den Dateipfad aus der Fehlermeldung hier einfügen:", font=("Segoe UI", 10)
)
lbl_instruction.pack(pady=(15, 5), padx=20, anchor="w")

# Eingabefeld
entry_path = tk.Entry(root, font=("Segoe UI", 10))
entry_path.pack(fill="x", padx=20, pady=5)
entry_path.focus_set()

# Enter-Taste im Eingabefeld löst ebenfalls die Aktion aus
entry_path.bind("<Return>", lambda event: process_deletion())

# Button-Leiste
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=(15, 10))

btn_confirm = tk.Button(
    frame_buttons,
    text="Ordner löschen",
    command=process_deletion,
    width=16,
    bg="#d9534f",
    fg="white",
    font=("Segoe UI", 9, "bold"),
)
btn_confirm.pack(side="left", padx=10)

btn_cancel = tk.Button(
    frame_buttons,
    text="Abbrechen",
    command=root.destroy,
    width=12,
    font=("Segoe UI", 9),
)
btn_cancel.pack(side="left", padx=10)

root.mainloop()