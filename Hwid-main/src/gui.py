import tkinter as tk
from tkinter import messagebox
from .logic import generate_hwid

class HWIDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HWID")
        self.root.geometry("320x105")
        self.root.resizable(False, False)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        self._center_window()

        lbl_title = tk.Label(root, text="Generador de HWID", font=("Arial", 9, "bold"))
        lbl_title.pack(pady=(5, 1))

        frame_hwid = tk.Frame(root)
        frame_hwid.pack(pady=2)

        lbl_hwid = tk.Label(frame_hwid, text="HWID:", font=("Arial", 8))
        lbl_hwid.pack(side=tk.LEFT, padx=(0, 2))

        self.entry_hwid = tk.Entry(frame_hwid, width=28, font=("Consolas", 8), state="readonly")
        self.entry_hwid.pack(side=tk.LEFT)

        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=3)

        btn_generate = tk.Button(frame_buttons, text="Generar", command=self._on_generate, width=8, bg="#4CAF50", fg="white", font=("Arial", 8))
        btn_generate.pack(side=tk.LEFT, padx=2)

        btn_copy = tk.Button(frame_buttons, text="Copiar", command=self._on_copy, width=8, bg="#2196F3", fg="white", font=("Arial", 8))
        btn_copy.pack(side=tk.LEFT, padx=2)

        lbl_info = tk.Label(root, text="BIOS · Placa · Disco", font=("Arial", 6), fg="gray")
        lbl_info.pack(pady=(0, 2))

    def _center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _on_generate(self):
        try:
            hwid = generate_hwid()
            self.entry_hwid.config(state="normal")
            self.entry_hwid.delete(0, tk.END)
            self.entry_hwid.insert(0, hwid)
            self.entry_hwid.config(state="readonly")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el HWID.\nDetalles: {e}")

    def _on_copy(self):
        hwid_text = self.entry_hwid.get()
        if hwid_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(hwid_text)
            self.root.update()
            messagebox.showinfo("Copiado", "HWID copiado al portapapeles correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Primero genera un HWID antes de copiarlo.")

if __name__ == "__main__":
    root = tk.Tk()
    app = HWIDApp(root)
    root.mainloop()