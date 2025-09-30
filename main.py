import tkinter as tk
from gui.main_window import NetworkGUI

def main():
    root = tk.Tk()
    app = NetworkGUI(root)

    def on_closing():
        app.message_queue.put("QUIT")
        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()