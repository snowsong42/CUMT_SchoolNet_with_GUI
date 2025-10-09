import json
import os
import sys
import tkinter.messagebox as messagebox

class SettingsManager:
    def __init__(self):
        # 定义运营商后缀映射
        self.network_type_mapping = {
            "1.移动": "@cmcc",
            "2.联通": "@unicom",
            "3.电信": "@telecom",
            "4.校园网": ""
        }

    def get_settings_path(self):
        """获取设置文件路径"""
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, "../UserData/network_settings.json")

    def load_settings(self, app):
        """加载保存的设置"""
        settings_path = self.get_settings_path()
        try:
            if os.path.exists(settings_path):
                with open(settings_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)

                # 获取保存的账号信息
                account_number = settings.get('account', '')
                password = settings.get('password', '')
                saved_network_type = settings.get('network_type', '4.校园网')  # 默认为校园网

                # 设置界面组件信息
                app.ui_components['account_var'].set(account_number)
                app.ui_components['password_var'].set(password)
                app.ui_components['combobox'].set(saved_network_type)

                # 细节，更新后缀显示
                suffix_text = self.network_type_mapping.get(saved_network_type, "@unicom")
                app.ui_components['account_suffix'].config(text=suffix_text)

                app.thread_handler.log_message("设置加载成功")
            else:
                # 默认值
                app.ui_components['account_var'].set("")
                app.ui_components['password_var'].set("")
                app.ui_components['combobox'].set("")
                app.ui_components['account_suffix'].config(text="")
                app.thread_handler.log_message("使用默认设置")

        except Exception as e:
            app.thread_handler.log_message(f"加载设置失败: {e}")
            # 设置默认值
            app.ui_components['account_var'].set("")
            app.ui_components['password_var'].set("")
            app.ui_components['combobox'].set("")
            app.ui_components['account_suffix'].config(text="")

    def save_settings(self, app):
        """保存设置到文件"""
        try:
            account_number = app.ui_components['account_var'].get().strip()
            password = app.ui_components['password_var'].get()
            selected_network = app.ui_components['combobox'].get()

            if not account_number:
                messagebox.showerror("账号不能为空！", "错误")
                return

            settings = {
                'account': account_number,
                'password': password,
                'network_type': selected_network
            }

            settings_path = self.get_settings_path()
            os.makedirs(os.path.dirname(settings_path), exist_ok=True)
            with open(settings_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)

            app.thread_handler.log_message("设置保存成功")
            messagebox.showerror("设置已保存！", "成功")

        except Exception as e:
            app.thread_handler.log_message(f"保存设置失败: {e}")
            messagebox.showerror(f"保存设置失败: {e}", "错误")