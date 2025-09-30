import json
import os
import sys
import pyautogui as pg

class SettingsManager:
    def __init__(self):
        pass

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

                # 从完整账号中提取数字部分
                full_account = settings.get('account', '')
                if '@unicom' in full_account:
                    account_number = full_account.split('@')[0]
                    app.ui_components['account_var'].set(account_number)
                else:
                    app.ui_components['account_var'].set(full_account)

                app.ui_components['password_var'].set(settings.get('password', ''))
                app.thread_handler.log_message("设置加载成功")
            else:
                # 默认值
                app.ui_components['account_var'].set(" ")
                app.ui_components['password_var'].set(" ")
                app.thread_handler.log_message("使用默认设置")

        except Exception as e:
            app.thread_handler.log_message(f"加载设置失败: {e}")
            # 设置默认值
            app.ui_components['account_var'].set("06245011")
            app.ui_components['password_var'].set("Snowsong_42")

    def save_settings(self, app):
        """保存设置到文件"""
        try:
            account_number = app.ui_components['account_var'].get().strip()
            password = app.ui_components['password_var'].get()

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
            os.makedirs(os.path.dirname(settings_path), exist_ok=True)
            with open(settings_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)

            app.thread_handler.log_message("设置保存成功")
            pg.alert("设置已保存！", "成功")

        except Exception as e:
            app.thread_handler.log_message(f"保存设置失败: {e}")
            pg.alert(f"保存设置失败: {e}", "错误")