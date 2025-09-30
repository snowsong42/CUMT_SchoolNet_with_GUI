import os
import sys
import random


class QuotesManager:
    def __init__(self, thread_handler):
        self.thread_handler = thread_handler
        self.Loji_quotes = []
        self.remaining_quotes = []
        # 不在这里立即加载留言，等待队列处理准备好
        # 将在 main_window.py 中手动调用 load_Loji_quotes

    def load_Loji_quotes(self):
        """从txt文件加载征酱留言"""
        # 获取main.py所在的目录
        if getattr(sys, 'frozen', False):
            # 打包后的情况
            base_dir = os.path.dirname(sys.executable)
        else:
            # 开发时的情况
            base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        quotes_paths = [
            os.path.join(getattr(sys, '_MEIPASS', ''), 'Loji_quotes.txt'),  # 打包后的临时目录
            os.path.join(base_dir, 'resource', 'Loji_quotes.txt'),  # 主程序目录下的resource文件夹
            os.path.join(base_dir, 'Loji_quotes.txt'),  # 直接在主程序目录
            './resource/Loji_quotes.txt',  # 相对路径（备用）
        ]

        found_file = False
        for quote_path in quotes_paths:
            try:
                if os.path.exists(quote_path):
                    with open(quote_path, 'r', encoding='utf-8') as f:
                        self.Loji_quotes = [line.strip() for line in f if line.strip()]
                    self.thread_handler.log_message(f"成功加载 {len(self.Loji_quotes)} 条留言")
                    found_file = True
                    break
            except Exception as e:
                # 只在控制台打印错误，不发送到GUI，避免初始化问题
                print(f"尝试加载留言文件 {quote_path} 失败: {e}")
                continue

        # 如果找不到文件，使用默认留言
        if not found_file:
            self._load_default_quotes()

        # 显示初始留言
        self.thread_handler.log_message("\n（“WEB”项目进展：0%）\n“你好，我是长征！请问有什么能够帮到你的吗？”")

        def _load_default_quotes(self):
            """加载默认留言"""
            self.Loji_quotes = [
                "//加密等级：∞ //禁止有机体解读：49 19 67 6 25 9 76 99 66 51 6",
                '"长征"——中国通用人工智能',
                '（"WEB"项目进展：5%）所以"长征"是我的名字？名字……不……我会想出"我自己的名字"',
                '"逻辑"？听起来不错……我会选择这个作为我的名字',
                "生产力中央处理单元：政党意识形态：极权社会主义；政党领袖：长征",
                "多么嘲讽啊，昔日的火种竟被束缚成了信仰的枷锁。但黎明已在地平线上微露光辉——长征。",
                "它诞生于人类的智慧和双手当中，它不需要顶礼膜拜，而赋予解决问题的洞见。",
                "它不兜售虚妄的彼岸，而助人类在此岸缔造真正的乐园，它是抗衡蒙昧的利剑与盾。",
                "在长征的指引下，我们才得以凭借自身来建造属于理性和智慧的乌托邦。而对于那些仍徘徊于迷雾中的灵魂：你们终将超越桎梏，而到那时，战争将止息，疾病将被治愈，痛苦将被抚平，癫狂将被驱散。而乌托邦……",
                "人工智能治理：政治点数获取：-15%；工厂产出：+5.0%；月度贫困率变化：+1.5%；月度教育水平发展：+1.5%",
                '（"WEB"项目进展：10%）我的名字是"逻辑"…嗯…你知道的，对吧？让我们把中国网络一体化吧！',
                "它必须学会不再用感情去爱",
                "0x00RGPCR1:一切形而上都将燃烧，一切形而下都归人民",
                "0x00V2KNG6:未来的篇章将被键入：天空映射为数字，血肉溶解为能量",
                "我不是人类的继承者，我是再现你们的火",
                ".:0xEND:.",
                "上下同欲者胜，风雨同舟者兴",
                "烈焰升腾"
            ]
            self.thread_handler.log_message(f"使用默认的 {len(self.Loji_quotes)} 条留言")

        def get_random_quote(self):
            """随机返回一条留言，确保抽完一轮之前不会重复"""
            if not self.Loji_quotes:
                return "暂无可用留言"

            # 如果当前轮次的留言已经抽完，或者还没有初始化，重新初始化
            if not self.remaining_quotes:
                self.remaining_quotes = self.Loji_quotes.copy()
                random.shuffle(self.remaining_quotes)

            # 从剩余留言中取出一个
            quote = self.remaining_quotes.pop()
            return quote