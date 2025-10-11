import tkinter as tk
import ctypes


def main():
    # 设置DPI感知（仅Windows）
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

    root = tk.Tk()
    from gui.main_window import NetworkGUI
    app = NetworkGUI(root)

    def on_closing():
        app.message_queue.put("QUIT")
        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()