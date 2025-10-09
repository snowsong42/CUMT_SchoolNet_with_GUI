import time
import requests
from requests import get
import socket
import pyautogui as pg

class NetworkConnection:
    def __init__(self, thread_handler):
        self.thread_handler = thread_handler
        self.is_connecting = False

        # 配置信息

        self.login_url = "http://10.2.5.251:801/eportal/" # 入口
        self.local_ip = ""

    def start_connection(self, account_number, password,combobox):
        """启动连接过程"""
        self.is_connecting = True
        self.thread_handler.set_button_state("disabled", "连接中...")

        import threading
        connection_thread = threading.Thread(target=self._connect_network,
                                             args=(account_number, password,combobox))
        connection_thread.daemon = True
        connection_thread.start()

    def _connect_network(self, account_number, password,combobox):
        """连接网络的主函数"""
        try:
            self.thread_handler.log_message("“长征”：系统上线\n正在为您服务\n" + "=" * 20)

            # 获取实际的本机IP
            self.local_ip = self.get_local_ip()
            self.thread_handler.log_message(f"检测到本机IP: {self.local_ip}")

            full_account = account_number + combobox
            self.thread_handler.log_message(f"使用账号: {account_number}****")
            self.thread_handler.log_message(f"账号完整格式: {full_account}")

            # 准备登录数据
            #data = self._prepare_login_data(full_account, password)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
            }

            self.thread_handler.log_message("开始登录校园网认证...\n" + "=" * 20)

            # 发送登录请求
            param = {
                'c': 'Portal',
                'a': 'login',
                'login_method': '1',
                # 登陆账号
                'user_account': full_account,
                # 登录密码
                'user_password': password,
                'wlan_user_ip': self.local_ip,
            }
            response = get(url=self.login_url, params=param, headers=headers)

            #response = requests.post(self.login_url, data=data, headers=headers, timeout=10)
            self.thread_handler.log_message(f"登录请求状态码: {response.status_code}")
            self.thread_handler.log_message(f"登录响应内容:\n {response.text[:200]}...")

            # 处理登录响应
            self._handle_login_response(response)

        except requests.exceptions.Timeout:
            self._handle_connection_error("请求超时", "请求超时，请检查网络连接或服务器状态")
        except requests.exceptions.ConnectionError:
            self._handle_connection_error("网络连接错误", "网络连接错误，请检查网络设置")
        except requests.exceptions.RequestException as e:
            self._handle_connection_error(f"网络请求异常 - {e}", f"网络请求异常: {str(e)}")
        except Exception as e:
            self._handle_connection_error(f"发生未知错误 - {e}", f"发生未知错误: {str(e)}")
        finally:
            self._finish_connection()


    def _handle_login_response(self, response):
        """处理登录响应"""
        if response.status_code != 200:
            error_msg = f"登录失败！\n状态码: {response.status_code}\n请检查账号密码或网络设置"
            self.thread_handler.log_message(f"登录失败，状态码: {response.status_code}")
            self.thread_handler.show_alert('登录失败', error_msg, '重新尝试')
            return

        # 正常情况
        time.sleep(1)  # 等待登录生效
        # 检查互联网连接
        self.thread_handler.log_message("检查Internet连通性，尝试访问百度\n" + "=" * 20)
        if self.check_internet_connection():
            success_msg = f"登录成功！\n本机IP: {self.local_ip}\nInternet连接正常"
            self.thread_handler.log_message("网络登录成功，Internet连接正常")
            self.thread_handler.show_alert('连接成功(oﾟvﾟ)ノ', success_msg, '冲浪，冲！')
        else:
            warning_msg = f"登录请求已发送，但外部网络连接可能尚未建立\n状态码: {response.status_code}\n请稍后手动检查网络连接"
            self.thread_handler.log_message("登录请求成功，但外部互联网连接检查失败")
            self.thread_handler.show_alert('连接状态待确认', warning_msg, '知道了')

        # 检查校园网内部连接
        self.thread_handler.log_message("检查校园网内部连接，尝试矿大教务系统\n" + "=" * 20)
        if not self.check_local_network():
            self.thread_handler.log_message("错误: 无法连接到校园内网")
            self.thread_handler.show_alert('校园网连接错误',
                                           '无法连接到校园内网，请检查网络连接或联系网络管理员！',
                                           '确定')

    def _handle_connection_error(self, log_message, alert_message):
        """处理连接错误"""
        self.thread_handler.log_message(f"错误: {log_message}")
        self.thread_handler.show_alert('连接错误', alert_message, '确定')

    def _finish_connection(self):
        """完成连接过程"""
        self.thread_handler.log_message("")
        self.thread_handler.log_message("“长征”回报：连接过程执行完毕\n" + "=" * 20)
        self.thread_handler.show_random_quote()
        self.thread_handler.set_button_state("normal", "连接网络")
        self.is_connecting = False

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

    def check_internet_connection(self, timeout=5):
        """检查是否能够连接到百度（外部网络）"""
        host = "www.baidu.com" #百度
        try:
            response = requests.get(host, timeout=timeout)
            if response.status_code == 200:
                self.thread_handler.log_message(f"✓ 外部网络连接正常\n成功访问 {host}")
                return True
            else:
                self.thread_handler.log_message(f"✗ 外部网络连接异常\n {host} 返回状态码: {response.status_code}")
                return False
        except Exception as e:
            self.thread_handler.log_message(f"✗ 外部网络连接失败\n无法访问 {host}: {e}")
            return False

    def check_local_network(self, timeout=5):
        """检查校园网内部网络连接 - 连接到矿大教务系统"""
        host = "http://jwxt.cumt.edu.cn/jwglxt/xtgl/login_slogin.html" # 教务系统
        try:
            response = requests.get(host, timeout=timeout)
            if response.status_code == 200:
                self.thread_handler.log_message(f"✓ 校园网内部连接正常\n成功访问 {host}")
                return True
            else:
                self.thread_handler.log_message(f"✗ 校园网内部连接异常\n {host} 返回状态码: {response.status_code}")
                return False
        except Exception as e:
            self.thread_handler.log_message(f"✗ 校园网内部连接失败\n无法访问 {host}: {e}")
            return False