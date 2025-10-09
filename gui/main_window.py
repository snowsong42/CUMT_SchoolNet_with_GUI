import tkinter as tk
import tkinter.messagebox as messagebox
import queue

from gui.components import create_main_interface
from network.connection import NetworkConnection
from utils.settings import SettingsManager
from utils.quotes_manager import QuotesManager
from utils.threading_utils import ThreadSafeMessageHandler


class NetworkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("自动登录矿大校园网")
        self.root.geometry("600x600")
        self.root.resizable(True, True)

        # 首先创建消息队列
        self.message_queue = queue.Queue()

        # 然后初始化管理器
        self.thread_handler = ThreadSafeMessageHandler(self)
        self.settings_manager = SettingsManager()
        self.quotes_manager = QuotesManager(self.thread_handler)

        # 初始化网络连接
        self.network_connection = NetworkConnection(self.thread_handler)

        # 创建UI - 传递 thread_handler
        self.ui_components = create_main_interface(self.root, self, self.thread_handler)

        # 加载设置
        self.settings_manager.load_settings(self)

        # 启动队列处理
        self.thread_handler.start_queue_processing()

        # 延迟加载留言，确保队列处理已经启动
        self.root.after(200, self.delayed_load_quotes)

    def delayed_load_quotes(self):
        """延迟加载留言，确保消息队列处理已经启动"""
        self.quotes_manager.load_Loji_quotes()

    def show_Loji_words(self):
        quote = self.quotes_manager.get_random_quote()
        self.thread_handler.log_message(f"{quote}")

    def save_settings(self):
        self.settings_manager.save_settings(self)

    def safe_quit(self):
        """安全退出程序"""
        self.root.quit()
        self.root.destroy()

    def clear_log(self):
        """清空日志"""
        self.ui_components['log_text'].config(state=tk.NORMAL)
        self.ui_components['log_text'].delete(1.0, tk.END)
        self.ui_components['log_text'].config(state=tk.DISABLED)

    def start_connection_thread(self):
        """在新线程中启动连接过程"""
        # 1. 验证输入
        # 2. 创建新线程
        # 3. 在新线程中执行网络连接
        if self.network_connection.is_connecting:
            self.thread_handler.log_message("Now loading...")
            return

        # 验证输入
        account_number = self.ui_components['account_var'].get().strip()
        password = self.ui_components['password_var'].get()

        selected_value = self.ui_components['combobox'].get()
        account_suffix = ""
        # 根据选择更新账号后缀
        if selected_value == "1.移动":
            self.ui_components['account_suffix'].config(text="@cmcc")
            account_suffix = "@cmcc"
        elif selected_value == "2.联通":
            self.ui_components['account_suffix'].config(text="@unicom")
            account_suffix = "@unicom"
        elif selected_value == "3.电信":
            self.ui_components['account_suffix'].config(text="@telecom")
            account_suffix = "@telecom"
        elif selected_value == "4.校园网":
            self.ui_components['account_suffix'].config(text="")
            account_suffix = ""

        if not account_number:
            import pyautogui as pg
            messagebox.showerror("请输入账号！", "错误")
            return
        if not password:
            import pyautogui as pg
            messagebox.showerror("请输入密码！", "错误")
            return

        # 见connection.py
        self.network_connection.start_connection(account_number, password, account_suffix)