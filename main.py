from gui import MillionaireGame
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()

    # Центрирование окна на экране
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (1000 // 2)
    y = (root.winfo_screenheight() // 2) - (700 // 2)
    root.geometry(f"1000x700+{x}+{y}")

    game = MillionaireGame(root)
    root.mainloop()