import tkinter as tk
from tkinter import scrolledtext
import os
import sys

def set_window_icon(root):
    """设置窗口图标，支持打包和未打包两种模式"""

    # 获取main.py所在的目录
    if getattr(sys, 'frozen', False):
        # 打包后的情况
        base_dir = os.path.dirname(sys.executable)
    else:
        # 开发时的情况
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    
    icon_paths = [
        os.path.join(getattr(sys, '_MEIPASS', ''), '矿大LOGO_1024x1024.ico'),  # 打包后的临时目录
        os.path.join(base_dir, 'resource', '矿大LOGO_1024x1024.ico'),  # 主程序目录下的resources文件夹
        os.path.join(base_dir, '矿大LOGO_1024x1024.ico'),  # 直接在主程序目录
        './resource/Loji_quotes.txt',  # 相对路径（备用）
    ]

    for icon_path in icon_paths:
        try:
            if os.path.exists(icon_path):
                root.iconbitmap(icon_path)
                print(f"成功加载图标,从路径: {icon_path}")
                return
        except Exception as e:
            print(f"尝试加载图标 {icon_path} 失败: {e}")
            continue

    print("警告: 无法加载任何图标文件，将使用默认图标")

def create_main_interface(root, app):
    """创建主界面组件"""
    set_window_icon(root)

    components = {}

    # 创建主框架
    main_frame = tk.Frame(root, padx=10, pady=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # 标题
    title_label = tk.Label(main_frame, text="自动登录矿大校园网", font=("宋体", 12, "bold"))
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

    components['account_var'] = tk.StringVar()
    components['account_entry'] = tk.Entry(account_input_frame, textvariable=components['account_var'], width=15)
    components['account_entry'].pack(side=tk.LEFT)

    account_suffix = tk.Label(account_input_frame, text="@unicom")
    account_suffix.pack(side=tk.LEFT, padx=(5, 0))

    # 密码输入行
    password_frame = tk.Frame(login_frame)
    password_frame.pack(fill=tk.X, pady=5)

    password_label = tk.Label(password_frame, text="密码:", width=8, anchor="e")
    password_label.pack(side=tk.LEFT)

    components['password_var'] = tk.StringVar()
    components['password_entry'] = tk.Entry(password_frame, textvariable=components['password_var'], show="*", width=25)
    components['password_entry'].pack(side=tk.LEFT)

    # 状态显示区域
    status_frame = tk.LabelFrame(main_frame, text="通信记录", padx=10, pady=10)
    status_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    # 滚动文本框用于显示详细信息
    components['log_text'] = scrolledtext.ScrolledText(status_frame, height=15, width=70)
    components['log_text'].pack(fill=tk.BOTH, expand=True)
    components['log_text'].config(state=tk.DISABLED)

    # 按钮框架
    button_frame = tk.Frame(main_frame)
    button_frame.pack(pady=10)

    # 连接按钮
    components['connect_button'] = tk.Button(button_frame, text="连接网络",
                                             command=app.start_connection_thread,
                                             bg="lightblue", font=("宋体", 12))
    components['connect_button'].pack(side=tk.LEFT, padx=5)

    # 保存设置按钮
    save_button = tk.Button(button_frame, text="保存设置",
                            command=app.save_settings,
                            bg="lightgreen", font=("宋体", 12))
    save_button.pack(side=tk.LEFT, padx=5)

    # 读取留言按钮
    save_button = tk.Button(button_frame, text="读取“长征”留言",
    command = app.show_Loji_words,
    bg = "lightgreen", font = ("宋体", 12))
    save_button.pack(side=tk.LEFT, padx=5)

    # 清空日志按钮
    clear_button = tk.Button(button_frame, text="清空日志",
                             command=app.clear_log,
                             bg="lightyellow", font=("宋体", 12))
    clear_button.pack(side=tk.LEFT, padx=5)

    # 退出按钮
    exit_button = tk.Button(button_frame, text="退出",
                            command=app.safe_quit,
                            bg="lightcoral", font=("宋体", 12))
    exit_button.pack(side=tk.LEFT, padx=5)

    return components