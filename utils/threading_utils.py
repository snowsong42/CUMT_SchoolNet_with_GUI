import tkinter as tk
import time
import pyautogui as pg

class ThreadSafeMessageHandler:
    def __init__(self, app):
        self.app = app
        # 不再在这里直接访问 app.message_queue
        # 改为在 start_queue_processing 中设置
        self.message_queue = None

    def start_queue_processing(self):
        """启动队列处理"""
        # 在这里设置 message_queue，确保它已经被创建
        self.message_queue = self.app.message_queue
        self.process_queue()

    def process_queue(self):
        """处理来自其他线程的消息队列"""
        if self.message_queue is None:
            return

        try:
            while True:
                message = self.message_queue.get_nowait()
                if message == "QUIT":
                    break
                elif isinstance(message, tuple):
                    method, args = message
                    if method == "log":
                        self._log_message(args[0])
                    elif method == "button_state":
                        self._set_button_state(args[0], args[1])
                    elif method == "alert":
                        self._show_alert(args[0], args[1], args[2])
                    elif method == "random_quote":
                        self._show_random_quote()
        except:
            pass
        finally:
            self.app.root.after(100, self.process_queue)

    def _log_message(self, message):
        """线程安全的日志记录（内部方法）"""
        self.app.ui_components['log_text'].config(state=tk.NORMAL)
        self.app.ui_components['log_text'].insert(tk.END, f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.app.ui_components['log_text'].see(tk.END)
        self.app.ui_components['log_text'].config(state=tk.DISABLED)

    def _set_button_state(self, state, text):
        """线程安全的按钮状态设置（内部方法）"""
        self.app.ui_components['connect_button'].config(state=state, text=text)

    def _show_alert(self, title, text, button):
        """线程安全的弹窗显示（内部方法）"""
        pg.alert(title=title, text=text, button=button)

    def _show_random_quote(self):
        """线程安全的显示随机留言（内部方法）"""
        quote = self.app.quotes_manager.get_random_quote()
        self._log_message(f"{quote}")

    def log_message(self, message):
        """线程安全的日志记录"""
        if self.message_queue is not None:
            self.message_queue.put(("log", [message]))

    def set_button_state(self, state, text):
        """线程安全的按钮状态设置"""
        if self.message_queue is not None:
            self.message_queue.put(("button_state", [state, text]))

    def show_alert(self, title, text, button):
        """线程安全的弹窗显示"""
        if self.message_queue is not None:
            self.message_queue.put(("alert", [title, text, button]))

    def show_random_quote(self):
        """线程安全的显示随机留言"""
        if self.message_queue is not None:
            self.message_queue.put(("random_quote", []))