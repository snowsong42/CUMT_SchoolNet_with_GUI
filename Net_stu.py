import requests
import pyautogui as pg
import time
import socket
import tkinter as tk
from tkinter import scrolledtext
import threading
import queue

class NetworkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("自动登录矿大校园网")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        self.root.iconbitmap("矿大LOGO_1024x1024.ico")

        # 创建一个队列用于线程间通信
        self.message_queue = queue.Queue()

        # 创建主框架
        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        title_label = tk.Label(main_frame, text="通信记录",
                               font=("宋体", 12, "bold"))
        title_label.pack(pady=10)

        # 状态显示区域
        status_frame = tk.LabelFrame(main_frame, text="连接状态", padx=10, pady=10)
        status_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # 滚动文本框用于显示详细信息
        self.log_text = scrolledtext.ScrolledText(status_frame, height=15, width=70)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)

        # 按钮框架
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)

        # 连接按钮
        self.connect_button = tk.Button(button_frame, text="连接网络",
                                        command=self.start_connection_thread,
                                        bg="lightblue", font=("宋体", 12))
        self.connect_button.pack(side=tk.LEFT, padx=5)

        # 清空日志按钮
        clear_button = tk.Button(button_frame, text="清空日志",
                                 command=self.clear_log,
                                 bg="lightyellow", font=("宋体", 12))
        clear_button.pack(side=tk.LEFT, padx=5)

        # 退出按钮
        exit_button = tk.Button(button_frame, text="退出",
                                command=self.safe_quit,
                                bg="lightcoral", font=("宋体", 12))
        exit_button.pack(side=tk.LEFT, padx=5)

        # 配置信息
        self.url = "http://10.2.5.251:801/"
        self.login_url = "http://10.2.5.251:801/"
        self.local_ip = ""

        # 线程控制
        self.connection_thread = None
        self.is_connecting = False

        # 启动队列处理
        self.process_queue()

    def safe_quit(self):
        """安全退出程序"""
        self.root.quit()
        self.root.destroy()

    def process_queue(self):
        """处理来自其他线程的消息队列"""
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
        except queue.Empty:
            pass
        finally:
            # 每100毫秒检查一次队列
            self.root.after(100, self.process_queue)

    def _log_message(self, message):
        """线程安全的日志记录（内部方法）"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def _set_button_state(self, state, text):
        """线程安全的按钮状态设置（内部方法）"""
        self.connect_button.config(state=state, text=text)

    def log_message(self, message):
        """线程安全的日志记录"""
        self.message_queue.put(("log", [message]))

    def set_button_state(self, state, text):
        """线程安全的按钮状态设置"""
        self.message_queue.put(("button_state", [state, text]))

    def clear_log(self):
        """清空日志"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)

    def check_internet_connection(self, host="8.8.8.8", port=53, timeout=3):
        """检查是否能够连接到互联网"""
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error:
            return False

    def check_local_network(self, url, timeout=5):
        """检查本地网络连接"""
        try:
            response = requests.get(url, timeout=timeout)
            return response.status_code == 200
        except:
            return False

    def get_local_ip(self):
        """获取本机IP地址"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "无法获取IP"

    def start_connection_thread(self):
        """在新线程中启动连接过程"""
        if self.is_connecting:
            self.log_message("连接正在进行中，请稍候...")
            return

        self.is_connecting = True
        self.set_button_state(tk.DISABLED, "连接中...")
        self.connection_thread = threading.Thread(target=self.connect_network)
        self.connection_thread.daemon = True
        self.connection_thread.start()

    def connect_network(self):
        """连接网络的主函数"""
        try:
            self.log_message("开始网络连接检查...")

            # 获取实际的本机IP
            self.local_ip = self.get_local_ip()
            self.log_message(f"检测到本机IP: {self.local_ip}")

            # 更新数据中的IP地址
            data = {
                "c": "Portal",
                "a": "login",
                "callback": "dr1759114957067",
                "login_method": "1",
                "user_account": "06245011@unicom",
                "user_password": "Snowsong_42",
                "wlan_user_ip": self.local_ip,
                "wlan_user_mac": "000000000000",
                "wlan_ac_ip": "wlan_ac_name",
                "jsVersion": "3.0",
                "_": str(int(time.time() * 1000))
            }

            # 请求头
            headers = {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection": "keep-alive",
                "Cookie": "PHPSESSID=4kpirs4g4r5es03v8776pdf5d4",
                "Host": "10.2.5.251:801",
                "Referer": "http://10.2.5.251/",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
            }

            # 检查本地网络连接
            if not self.check_local_network(self.url):
                self.log_message("错误: 无法连接到校园网络")
                # 使用 after 方法在主线程中显示弹窗
                self.root.after(0, lambda: pg.alert(
                    title='网络错误',
                    text='无法连接到校园网络，请检查网络连接！',
                    button='确定'
                ))
                return

            self.log_message("本地网络连接正常，开始登录...")

            # 发送登录请求
            response = requests.post(self.login_url, data=data, headers=headers, timeout=10)
            self.log_message(f"登录请求状态码: {response.status_code}")
            self.log_message(f"登录响应内容:\n {response.text[:200]}...")

            # 检查登录是否成功
            if response.status_code == 200:
                # 等待一下让登录生效
                time.sleep(2)

                # 检查互联网连接
                self.log_message("检查互联网连接...")
                if self.check_internet_connection():
                    success_msg = f"登录成功！\n本机IP: {self.local_ip}"
                    self.log_message("网络登录成功，互联网连接正常")
                    # 使用 after 方法在主线程中显示弹窗
                    self.root.after(0, lambda: pg.alert(
                        title='连接成功(oﾟvﾟ)ノ',
                        text=success_msg,
                        button='冲浪,冲！'
                    ))
                else:
                    warning_msg = f"登录请求已发送，但互联网连接可能尚未建立\n状态码: {response.status_code}\n请稍后手动检查网络连接"
                    self.log_message("登录请求成功，但互联网连接检查失败")
                    # 使用 after 方法在主线程中显示弹窗
                    self.root.after(0, lambda: pg.alert(
                        title='连接状态待确认',
                        text=warning_msg,
                        button='知道了'
                    ))
            else:
                error_msg = f"登录失败！\n状态码: {response.status_code}\n请检查账号密码或网络设置"
                self.log_message(f"登录失败，状态码: {response.status_code}")
                # 使用 after 方法在主线程中显示弹窗
                self.root.after(0, lambda: pg.alert(
                    title='登录失败',
                    text=error_msg,
                    button='重新尝试'
                ))

        except requests.exceptions.Timeout:
            self.log_message("错误: 请求超时")
            self.root.after(0, lambda: pg.alert(
                title='请求超时',
                text='请求超时，请检查网络连接或服务器状态',
                button='确定'
            ))

        except requests.exceptions.ConnectionError:
            self.log_message("错误: 网络连接错误")
            self.root.after(0, lambda: pg.alert(
                title='连接错误',
                text='网络连接错误，请检查网络设置',
                button='确定'
            ))

        except requests.exceptions.RequestException as e:
            self.log_message(f"错误: 网络请求异常 - {e}")
            self.root.after(0, lambda: pg.alert(
                title='请求异常',
                text=f'网络请求异常: {str(e)}',
                button='确定'
            ))

        except Exception as e:
            self.log_message(f"错误: 发生未知错误 - {e}")
            self.root.after(0, lambda: pg.alert(
                title='未知错误',
                text=f'发生未知错误: {str(e)}',
                button='确定'
            ))

        finally:
            self.log_message("连接过程执行完毕")
            self.set_button_state(tk.NORMAL, "连接网络")
            self.is_connecting = False


def main():
    root = tk.Tk()
    app = NetworkGUI(root)

    # 设置窗口关闭事件
    def on_closing():
        app.message_queue.put("QUIT")
        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()