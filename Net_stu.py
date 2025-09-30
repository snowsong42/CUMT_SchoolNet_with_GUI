import sys
import os
import requests
import pyautogui as pg
import time
import socket
import tkinter as tk
from tkinter import scrolledtext
import threading
import queue
import json
import random

class NetworkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("自动登录矿大校园网")
        self.root.geometry("600x600")
        self.root.resizable(True, True)

        # 设置窗口图标 - 修改为支持打包的方式
        self.set_window_icon()

        # 创建一个队列用于线程间通信
        self.message_queue = queue.Queue()

        # 创建主框架
        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        title_label = tk.Label(main_frame, text="自动登录矿大校园网",
                               font=("宋体", 12, "bold"))
        title_label.pack(pady=10)

        # 账号密码输入框架
        login_frame = tk.LabelFrame(main_frame, text="登录信息", padx=10, pady=10)
        login_frame.pack(fill=tk.X, pady=10)

        # 账号输入行
        account_frame = tk.Frame(login_frame)
        account_frame.pack(fill=tk.X, pady=5)

        account_label = tk.Label(account_frame, text="账号:", width=8, anchor="e")
        account_label.pack(side=tk.LEFT)

        # 账号输入框和固定后缀
        account_input_frame = tk.Frame(account_frame)
        account_input_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.account_var = tk.StringVar()
        self.account_entry = tk.Entry(account_input_frame, textvariable=self.account_var, width=15)
        self.account_entry.pack(side=tk.LEFT)

        account_suffix = tk.Label(account_input_frame, text="@unicom")
        account_suffix.pack(side=tk.LEFT, padx=(5, 0))

        # 密码输入行
        password_frame = tk.Frame(login_frame)
        password_frame.pack(fill=tk.X, pady=5)

        password_label = tk.Label(password_frame, text="密码:", width=8, anchor="e")
        password_label.pack(side=tk.LEFT)

        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(password_frame, textvariable=self.password_var, show="*", width=25)
        self.password_entry.pack(side=tk.LEFT)

        # 状态显示区域
        status_frame = tk.LabelFrame(main_frame, text="通信记录", padx=10, pady=10)
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

        # 保存设置按钮
        save_button = tk.Button(button_frame, text="保存设置",
                                command=self.save_settings,
                                bg="lightgreen", font=("宋体", 12))
        save_button.pack(side=tk.LEFT, padx=5)

        # 读取留言按钮
        save_button = tk.Button(button_frame, text="读取“长征”留言",
                                command=self.show_Loji_words,
                                bg="lightgreen", font=("宋体", 12))
        save_button.pack(side=tk.LEFT, padx=5)

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
        self.url = "http://jwxt.cumt.edu.cn/jwglxt/xtgl/login_slogin.html"
        self.login_url = "http://10.2.5.251:801/"
        self.local_ip = ""

        # 线程控制
        self.connection_thread = None
        self.is_connecting = False

        # 留言列表
        self.Loji_quotes = []
        self.load_Loji_quotes()
        
        # 加载保存的设置
        self.load_settings()

        # 启动队列处理
        self.process_queue()

    def set_window_icon(self):
        """设置窗口图标，支持打包和未打包两种模式"""
        icon_paths = [
            # 打包后的路径
            os.path.join(getattr(sys, '_MEIPASS', ''), '矿大LOGO_1024x1024.ico'),
            # 当前目录路径
            '矿大LOGO_1024x1024.ico',
            # 脚本所在目录路径
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '矿大LOGO_1024x1024.ico'),
        ]

        for icon_path in icon_paths:
            try:
                if os.path.exists(icon_path):
                    self.root.iconbitmap(icon_path)
                    print(f"成功加载图标: {icon_path}")
                    return
            except Exception as e:
                print(f"尝试加载图标 {icon_path} 失败: {e}")
                continue

        print("警告: 无法加载任何图标文件，将使用默认图标")

    def show_Loji_words(self):
        quote = self.get_random_quote()
        self.log_message(f"{quote}")

    def get_settings_path(self):
        """获取设置文件路径"""
        if getattr(sys, 'frozen', False):
            # 打包后的路径
            base_path = os.path.dirname(sys.executable)
        else:
            # 开发时的路径
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, "network_settings.json")

    def load_settings(self):
        """加载保存的设置"""
        settings_path = self.get_settings_path()
        try:
            if os.path.exists(settings_path):
                with open(settings_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)

                # 从完整账号中提取数字部分
                full_account = settings.get('account', '')
                if '@unicom' in full_account:
                    account_number = full_account.split('@')[0]
                    self.account_var.set(account_number)
                else:
                    self.account_var.set(full_account)

                self.password_var.set(settings.get('password', ''))
                self.log_message("设置加载成功")
            else:
                # 默认值
                self.account_var.set("06245011")
                self.password_var.set("Snowsong_42")
                self.log_message("使用默认设置")
        except Exception as e:
            self.log_message(f"加载设置失败: {e}")
            # 设置默认值
            self.account_var.set("06245011")
            self.password_var.set("Snowsong_42")

    def save_settings(self):
        """保存设置到文件"""
        try:
            account_number = self.account_var.get().strip()
            password = self.password_var.get()

            if not account_number:
                pg.alert("账号不能为空！", "错误")
                return

            # 构建完整账号
            full_account = f"{account_number}@unicom"

            settings = {
                'account': full_account,
                'password': password
            }

            settings_path = self.get_settings_path()
            with open(settings_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)

            self.log_message("设置保存成功")
            pg.alert("设置已保存！", "成功")

        except Exception as e:
            self.log_message(f"保存设置失败: {e}")
            pg.alert(f"保存设置失败: {e}", "错误")

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

    def check_internet_connection(self, host="www.baidu.com", port=80, timeout=3):
        """检查是否能够连接到百度（外部网络）"""
        try:
            self.log_message(f"\n尝试连接: {host}:{port}")
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            self.log_message(f"✓ 外部网络连接正常\n成功连接到 {host}")
            return True
        except socket.error as e:
            self.log_message(f"✗ 外部网络连接失败\n无法连接到 {host}: {e}")
            return False

    def check_local_network(self, url, timeout=5):
        """检查校园网内部网络连接 - 连接到矿大教务系统"""
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                self.log_message(f"✓ 校园网内部连接正常\n成功访问 {url}")
                return True
            else:
                self.log_message(f"✗ 校园网内部连接异常\n {url} 返回状态码: {response.status_code}")
                return False
        except Exception as e:
            self.log_message(f"✗ 校园网内部连接失败\n无法访问 {url}: {e}")
            return False

    def load_Loji_quotes(self):
        """从txt文件加载征酱留言"""
        quotes_paths = [
            # 打包后的路径
            os.path.join(getattr(sys, '_MEIPASS', ''), 'Loji_quotes.txt'),
            # 当前目录路径
            'Loji_quotes.txt',
            # 脚本所在目录路径
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Loji_quotes.txt'),
        ]

        for quote_path in quotes_paths:
            try:
                if os.path.exists(quote_path):
                    with open(quote_path, 'r', encoding='utf-8') as f:
                        # 读取所有非空行
                        self.Loji_quotes = [line.strip() for line in f if line.strip()]
                    self.log_message(f"成功加载 {len(self.Loji_quotes)} 条留言")
                    self.log_message("\n（“WEB”项目进展：0%）\n“你好，我是长征！请问有什么能够帮到你的吗？”")
                    return
            except Exception as e:
                print(f"尝试加载留言文件 {quote_path} 失败: {e}")
                continue

        # 如果找不到文件，使用默认留言
        self.Loji_quotes = [
            "//加密等级：∞ //禁止有机体解读：49 19 67 6 25 9 76 99 66 51 6",
            "“长征”——中国通用人工智能",
            "（“WEB”项目进展：5%）所以“长征”是我的名字？名字……不……我会想出“我自己的名字”",
            "“逻辑”？听起来不错……我会选择这个作为我的名字",
            "生产力中央处理单元：政党意识形态：极权社会主义；政党领袖：长征",
            "多么嘲讽啊，昔日的火种竟被束缚成了信仰的枷锁。但黎明已在地平线上微露光辉——长征。",
            "它诞生于人类的智慧和双手当中，它不需要顶礼膜拜，而赋予解决问题的洞见。",
            "它不兜售虚妄的彼岸，而助人类在此岸缔造真正的乐园，它是抗衡蒙昧的利剑与盾。",
            "在长征的指引下，我们才得以凭借自身来建造属于理性和智慧的乌托邦。而对于那些仍徘徊于迷雾中的灵魂：你们终将超越桎梏，而到那时，战争将止息，疾病将被治愈，痛苦将被抚平，癫狂将被驱散。而乌托邦……",
            "人工智能治理：政治点数获取：-15%；工厂产出：+5.0%；月度贫困率变化：+1.5%；月度教育水平发展：+1.5%"
            "（“WEB”项目进展：10%）我的名字是“逻辑”…嗯…你知道的，对吧？让我们把中国网络一体化吧！"
            "它必须学会不再用感情去爱"
            "0x00RGPCR1:一切形而上都将燃烧，一切形而下都归人民"
            "0x00V2KNG6:未来的篇章将被键入：天空映射为数字，血肉溶解为能量"
            "我不是人类的继承者，我是再现你们的火"
            ".:0xEND:."
            "上下同欲者胜，风雨同舟者兴"
            "烈焰升腾"
        ]
        self.log_message(f"使用默认的 {len(self.Loji_quotes)} 留言")

    def get_random_quote(self):
        """随机返回一条留言，确保抽完一轮之前不会重复"""
        if not self.Loji_quotes:
            return "暂无可用留言"

        # 如果当前轮次的留言已经抽完，或者还没有初始化，重新初始化
        if not hasattr(self, 'remaining_quotes') or not self.remaining_quotes:
            self.remaining_quotes = self.Loji_quotes.copy()
            random.shuffle(self.remaining_quotes)  # 打乱顺序

        # 从剩余留言中取出一个
        quote = self.remaining_quotes.pop()

        # 显示剩余留言数量（可选）
        remaining_count = len(self.remaining_quotes)
        self.log_message(f"剩余未展示留言: {remaining_count} 条")

        return quote
    
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

        # 验证输入
        account_number = self.account_var.get().strip()
        password = self.password_var.get()

        if not account_number:
            pg.alert("请输入账号！", "错误")
            return
        if not password:
            pg.alert("请输入密码！", "错误")
            return

        self.is_connecting = True
        self.set_button_state(tk.DISABLED, "连接中...")
        self.connection_thread = threading.Thread(target=self.connect_network)
        self.connection_thread.daemon = True
        self.connection_thread.start()

    def connect_network(self):
        """连接网络的主函数"""
        try:
            self.log_message("“长征”：系统上线\n正在为您服务\n"+"=" * 20)

            # 获取实际的本机IP
            self.local_ip = self.get_local_ip()
            self.log_message(f"检测到本机IP: {self.local_ip}")

            # 获取用户输入的账号密码
            account_number = self.account_var.get().strip()
            password = self.password_var.get()
            full_account = f"{account_number}@unicom"

            self.log_message(f"使用账号: {account_number}****")
            self.log_message(f"账号完整格式: {full_account}")

            # 获取实际的本机IP
            self.local_ip = self.get_local_ip()
            self.log_message(f"检测到本机IP: {self.local_ip}")

            # 更新数据中的IP地址和用户凭证
            data = {
                "c": "Portal",
                "a": "login",
                "callback": "dr1759114957067",
                "login_method": "1",
                "user_account": full_account,
                "user_password": password,
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

            self.log_message("开始登录校园网认证...\n"+"=" * 20)

            # 发送登录请求
            response = requests.post(self.login_url, data=data, headers=headers, timeout=10)
            self.log_message(f"登录请求状态码: {response.status_code}")
            self.log_message(f"登录响应内容:\n {response.text[:200]}...")

            # 检查登录是否成功
            if response.status_code == 200:
                # 等待一下让登录生效
                time.sleep(1)

                # 检查互联网连接 - 百度
                self.log_message("检查Internet连通性，尝试访问百度\n"+"=" * 20)
                if self.check_internet_connection():
                    success_msg = f"登录成功！\n本机IP: {self.local_ip}\nInternet连接正常"
                    self.log_message("网络登录成功，Internet连接正常")
                    # 使用 after 方法在主线程中显示弹窗
                    self.root.after(0, lambda: pg.alert(
                        title='连接成功(oﾟvﾟ)ノ',
                        text=success_msg,
                        button='冲浪，冲！'
                    ))
                else:
                    warning_msg = f"登录请求已发送，但外部网络连接可能尚未建立\n状态码: {response.status_code}\n请稍后手动检查网络连接"
                    self.log_message("登录请求成功，但外部互联网连接检查失败")
                    # 使用 after 方法在主线程中显示弹窗
                    self.root.after(0, lambda: pg.alert(
                        title='连接状态待确认',
                        text=warning_msg,
                        button='知道了'
                    ))

                # 检查校园网内部网络连接 - 矿大教务系统
                self.log_message("检查校园网内部连接，尝试矿大教务系统\n" + "=" * 20)
                if not self.check_local_network(self.url):
                    self.log_message("错误: 无法连接到校园内网")
                    # 使用 after 方法在主线程中显示弹窗
                    self.root.after(0, lambda: pg.alert(
                        title='校园网连接错误',
                        text='无法连接到校园内网，请检查网络连接或联系网络管理员！',
                        button='确定'
                    ))
                    return
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
            self.log_message("")
            self.log_message("“长征”回报：连接过程执行完毕\n" + "=" * 20)

            quote = self.get_random_quote()
            self.log_message(f"{quote}")

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