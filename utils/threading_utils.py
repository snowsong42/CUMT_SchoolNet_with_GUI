import tkinter as tk
import time
import queue
import pymsgbox

class ThreadSafeMessageHandler:
    def __init__(self, app):
        self.app = app
        self.message_queue = None

    def start_queue_processing(self):
        """启动队列处理"""
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
                    elif method == "print":
                        self._print_message(args[0])
                    elif method == "button_state":
                        self._set_button_state(args[0], args[1])
                    elif method == "alert":
                        self._show_alert(args[0], args[1], args[2])
                    elif method == "random_quote":
                        self._show_random_quote()
        except queue.Empty:  # 专门捕获队列空异常
            pass  # 这是正常情况，不需要处理
        except Exception as e:
            # 只记录真正的错误
            print(f"队列处理错误: {e}")
        finally:
            self.app.root.after(100, self.process_queue)

    def _log_message(self, message):
        """线程安全的日志记录（内部方法）"""
        try:
            self.app.ui_components['log_text'].config(state=tk.NORMAL)
            self.app.ui_components['log_text'].insert(tk.END, f"{time.strftime('%H:%M:%S')} - {message}\n")
            self.app.ui_components['log_text'].see(tk.END)
            self.app.ui_components['log_text'].config(state=tk.DISABLED)
        except Exception as e:
            print(f"日志记录失败: {e}")

    def _print_message(self, message):
        """线程安全的打印（内部方法）"""
        try:
            self.app.ui_components['log_text'].config(state=tk.NORMAL)
            self.app.ui_components['log_text'].insert(tk.END, f"{message}\n")
            self.app.ui_components['log_text'].see(tk.END)
            self.app.ui_components['log_text'].config(state=tk.DISABLED)
        except Exception as e:
            print(f"打印消息失败: {e}")

    def _set_button_state(self, state, text):
        """线程安全的按钮状态设置（内部方法）"""
        try:
            self.app.ui_components['connect_button'].config(state=state, text=text)
        except Exception as e:
            print(f"按钮状态设置失败: {e}")

    def _show_alert(self, title, text, button):
        """线程安全的弹窗显示（内部方法）"""
        pymsgbox.alert(text=text, title=title, button=button)

    def _show_random_quote(self):
        """线程安全的显示随机留言（内部方法）"""
        try:
            quote = self.app.quotes_manager.get_random_quote()
            self._log_message(f"{quote}")
        except Exception as e:
            print(f"显示随机留言失败: {e}")

    def log_message(self, message):
        """线程安全的日志记录"""
        if self.message_queue is not None:
            self.message_queue.put(("log", [message]))

    def print_message(self, message):
        """线程安全的日志记录"""
        if self.message_queue is not None:
            self.message_queue.put(("print", [message]))

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