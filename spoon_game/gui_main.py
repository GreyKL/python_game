# gui_main.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os
import time

from spoon_game import SpoonGame
from config import IMAGE_PATH, SPOON_NAMES, SPOONS_PER_TYPE, TOTAL_SPOON_TYPES, SPOON_PROBABILITIES


class SpoonGameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("掰勺子游戏")
        self.master.geometry("1200x800")  # 增加窗口宽度以容纳左侧面板

        self.game = SpoonGame()

        # 标记动画进行中
        self.animation_in_progress = False

        # 加载所有勺子图片（正常、掰弯、小图）
        self.load_images()

        # 消息文案池
        self.success_msgs = [
            "成功掰断！你真是超能力者！",
            "干得漂亮，又掰弯了一根！",
            "厉害！这根勺子也没逃过你的手心！"
        ]
        self.too_fast_msgs = [
            "慢点慢点，休息一下！",
            "急什么呢？先喘口气~",
            "太快了！保持专注~"
        ]
        self.end_msgs = [
            "游戏已结束！你已展示了无上的掰勺绝技！",
            "全部勺子都被你征服了，传奇诞生！",
            "恭喜你完成了所有挑战！"
        ]

        # 创建主容器框架
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill='both', expand=True)

        # 左侧勺子信息展示框架
        self.spoon_info_frame = tk.Frame(self.main_frame, padx=10, pady=10, bg="#f0f0f0")
        self.spoon_info_frame.pack(side='left', fill='y')

        # self.create_spoon_info()

        # 右侧游戏内容框架
        self.game_content_frame = tk.Frame(self.main_frame)
        self.game_content_frame.pack(side='right', fill='both', expand=True)

        # 结果显示Label（仅显示提示信息）
        self.result_label = tk.Label(self.game_content_frame, text="欢迎来到掰勺子游戏！", font=('Helvetica', 16, 'bold'), fg='blue', bg='white')
        self.result_label.pack(pady=(20,10))

        # 状态显示Label（显示当前种类与进度）
        self.status_label = tk.Label(self.game_content_frame, text=self.game.get_status(), font=('Helvetica', 14))
        self.status_label.pack(pady=10)

        # 中间区域：当前勺子的图片显示区域
        self.spoon_frame = tk.Frame(self.game_content_frame)
        self.spoon_frame.pack(pady=10)

        self.current_spoon_label = tk.Label(self.spoon_frame, image=self.current_spoon_image)
        self.current_spoon_label.pack()
        self.current_spoon_label.bind("<Button-1>", self.try_bend_spoon_action_event)  # 点击图片也能掰弯

        # 底部按钮区域
        self.button_frame = tk.Frame(self.game_content_frame)
        self.button_frame.pack(pady=10)

        # 在按钮区域添加“详情”按钮
        self.details_button = tk.Button(
            self.button_frame,
            text="详情",
            command=self.show_details,
            font=('Helvetica', 12)
        )
        self.details_button.grid(row=0, column=2, padx=10)

        # 添加玩法简介
        instruction_label = tk.Label(
            self.game_content_frame,
            text="玩法简介：点击图片或者按钮，又或者空格键掰勺子",
            font=('Helvetica', 12, 'italic'),
            fg="blue",
            wraplength=800,
            justify="left"
        )
        instruction_label.pack(pady=(10, 0))

        # 尝试掰弯按钮
        self.bend_button = tk.Button(self.button_frame, text="尝试掰弯勺子", command=self.try_bend_spoon_action, font=('Helvetica', 12))
        self.bend_button.grid(row=0, column=0, padx=10)

        # 退出按钮
        self.quit_button = tk.Button(self.button_frame, text="退出", command=self.quit_game, font=('Helvetica', 12))
        self.quit_button.grid(row=0, column=1, padx=10)

        # 绑定空格键事件，用空格也能触发掰勺子
        master.bind("<space>", self.try_bend_spoon_action_event)

        # 左下角已掰弯的勺子展示区域
        self.bent_spoons_frame = tk.Frame(self.game_content_frame)
        # 将其放置在左下角
        self.bent_spoons_frame.pack(side='bottom', anchor='w', padx=10, pady=10)

        self.bent_spoons_labels = {i: [] for i in range(1, TOTAL_SPOON_TYPES+1)}  # 每种类型的已掰弯勺子列表

        self.update_ui(initial=True)

    # 定义 show_details 方法
    def show_details(self):
        """显示所有勺子类型和对应的掰断概率的详情窗口"""
        details_window = tk.Toplevel(self.master)
        details_window.title("勺子详情")
        details_window.geometry("400x400")

        # 添加标题
        title_label = tk.Label(details_window, text="勺子详情", font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=10)

        # 创建一个可滚动的Canvas
        canvas = tk.Canvas(details_window)
        scrollbar = tk.Scrollbar(details_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Helper function to format probability as "1/n"
        def format_probability(p):
            if p > 0:
                denominator = int(1 / p)
                return f"1/{denominator}"
            else:
                return "0"

        # 添加每种勺子的名称和概率
        for i in range(1, TOTAL_SPOON_TYPES + 1):
            spoon_name = SPOON_NAMES.get(i, f"勺子{i}")
            probability = SPOON_PROBABILITIES.get(i, 0)
            probability_str = format_probability(probability)
            info_label = tk.Label(
                scrollable_frame,
                text=f"{i}. {spoon_name} - 掰断概率: {probability_str}",
                font=('Helvetica', 12),
                anchor='w'
            )
            info_label.pack(fill='x', pady=2)

    def load_images(self):
        """加载所有勺子的正常和掰弯状态图片，并生成小图标版本用于已掰弯展示"""
        self.spoon_images = {}
        self.spoon_bent_images = {}
        self.spoon_bent_small_images = {}

        # 主显示用大小
        main_size = (200, 200)
        # 左侧展示用小图
        small_size = (50, 50)

        for i in range(1, TOTAL_SPOON_TYPES+1):
            normal_path = os.path.join(IMAGE_PATH, f"spoon_{i:02d}.png")
            bent_path = os.path.join(IMAGE_PATH, f"spoon_{i:02d}_bent.png")

            try:
                normal_img = Image.open(normal_path).resize(main_size, Image.Resampling.LANCZOS)
                self.spoon_images[i] = ImageTk.PhotoImage(normal_img)

                bent_img = Image.open(bent_path).resize(main_size, Image.Resampling.LANCZOS)
                self.spoon_bent_images[i] = ImageTk.PhotoImage(bent_img)

                # 小图用于已掰弯勺子列表展示
                small_bent_img = Image.open(bent_path).resize(small_size, Image.Resampling.LANCZOS)
                self.spoon_bent_small_images[i] = ImageTk.PhotoImage(small_bent_img)

            except AttributeError:
                # Pillow 旧版本兼容
                normal_img = Image.open(normal_path).resize(main_size, Image.LANCZOS)
                self.spoon_images[i] = ImageTk.PhotoImage(normal_img)

                bent_img = Image.open(bent_path).resize(main_size, Image.LANCZOS)
                self.spoon_bent_images[i] = ImageTk.PhotoImage(bent_img)

                small_bent_img = Image.open(bent_path).resize(small_size, Image.LANCZOS)
                self.spoon_bent_small_images[i] = ImageTk.PhotoImage(small_bent_img)

            except Exception as e:
                messagebox.showerror("图片加载错误", f"无法加载图片：{normal_path} 或 {bent_path}\n错误信息：{e}")
                self.master.destroy()

        # 设置当前勺子的图片（初始为当前类型的正常图片）
        self.current_spoon_image = self.spoon_images[self.game.state.current_type]

        # 保存小图字典供后续使用
        self.spoon_bent_small_images_dict = self.spoon_bent_small_images

    def try_bend_spoon_action_event(self, event):
        """空格键或点击图片事件触发同样的动作"""
        self.try_bend_spoon_action()

    def try_bend_spoon_action(self):
        """尝试掰弯勺子的操作"""
        if self.animation_in_progress:
            # 如果动画正在进行中，暂时忽略点击
            return

        result = self.game.try_bend_spoon()
        msg_type = self.analyze_result_type(result)

        display_msg, fg_color = self.get_display_message_and_color(msg_type)
        self.result_label.config(text=display_msg, fg=fg_color)
        self.highlight_result_label()

        if msg_type == "success":
            # 掰弯成功后播放动画：
            # 1. 先显示弯曲状态图片
            self.animation_in_progress = True
            current_type = self.game.state.current_type
            # 显示当前类型的弯曲图片
            self.current_spoon_label.config(image=self.spoon_bent_images[current_type])

            # 0.5秒后切换到新的勺子（可能类型已更新）
            self.master.after(500, self.show_new_spoon_after_animation)
        else:
            # 失败或其他情况，正常更新UI
            self.update_ui()

    def show_new_spoon_after_animation(self):
        """动画结束后显示新的勺子（新类型或当前类型的正常勺子）"""
        self.animation_in_progress = False
        self.update_ui()

    def analyze_result_type(self, result):
        """根据返回结果判断消息类型"""
        if "成功掰断" in result or "恭喜" in result:
            if "游戏结束" in result:
                return "end"
            return "success"
        elif "太快" in result:
            return "too_fast"
        elif "失败" in result or "继续努力" in result:
            return "fail"
        elif "游戏已经结束" in result:
            return "end"
        else:
            # 为避免显示当前勺子类型，将默认返回 'fail' 或其他合适类型
            return "fail"

    def get_display_message_and_color(self, msg_type):
        """根据消息类型选择显示的文本和颜色"""
        if msg_type == "success":
            display_msg = random.choice(self.success_msgs)
            color = "green"
        elif msg_type == "fail":
            # 由于失败消息现在在 SpoonGame 中加载，这里不需要重新定义
            display_msg = random.choice(self.game.fail_msgs)
            color = "red"
        elif msg_type == "too_fast":
            display_msg = random.choice(self.too_fast_msgs)
            color = "orange"
        elif msg_type == "end":
            display_msg = random.choice(self.end_msgs)
            color = "purple"
        else:
            # 不应到达这里，但为了安全，可以设置默认
            display_msg = "未知状态。"
            color = "blue"
        return display_msg, color

    def highlight_result_label(self):
        """给 result_label 添加简单的闪烁动画效果"""
        original_bg = self.result_label.cget("bg")

        def flash(count=0):
            if count % 2 == 0:
                self.result_label.config(bg="yellow")
            else:
                self.result_label.config(bg=original_bg)
            if count < 6:
                self.master.after(150, lambda: flash(count+1))

        flash(0)

    def update_ui(self, initial=False):
        """更新界面显示，包括状态、已掰弯的勺子展示和当前勺子图片"""

        current_status = self.game.get_status()
        self.status_label.config(text=current_status)

        # 如果动画未进行中才更新主勺子图片
        if not self.animation_in_progress:
            # 显示当前类型正常状态的勺子
            current_type = self.game.state.current_type
            self.current_spoon_label.config(image=self.spoon_images[current_type])

        # 更新已掰弯的勺子展示区域
        # 需求：显示所有已掰弯的勺子。
        # 第一行显示类型1的已掰弯勺子（共10个或不足10个则显示实际数量）,
        # 第二行显示类型2的已掰弯勺子，如此类推。
        # 每行最多10个勺子(刚好SPOONS_PER_TYPE=10)。
        # 已掰弯的勺子从self.game.state.bent_spoons中获取数量

        # 清空当前展示
        for t in range(1, TOTAL_SPOON_TYPES+1):
            for label in self.bent_spoons_labels[t]:
                label.destroy()
            self.bent_spoons_labels[t] = []

        # 重新布局已掰弯勺子
        # 类型t在第(t-1)行，从bent_spoons中读取数量count
        # 显示count个小图标
        for t in range(1, TOTAL_SPOON_TYPES+1):
            count = self.game.state.bent_spoons.get(str(t), 0)
            if count > 0:
                # 显示count个小图标，最多SPOONS_PER_TYPE个
                display_count = min(count, SPOONS_PER_TYPE)
                for j in range(display_count):
                    bent_img_small = self.spoon_bent_small_images_dict[t]
                    label = tk.Label(self.bent_spoons_frame, image=bent_img_small)
                    # t-1行，j列
                    label.grid(row=t-1, column=j, padx=2, pady=2)
                    self.bent_spoons_labels[t].append(label)
                # 如果有超过SPOONS_PER_TYPE的勺子，可以考虑添加分页或其他展示方式
                # 这里暂不处理，假设SPOONS_PER_TYPE=10

        # 如果游戏已结束，禁用按钮并提示
        if self.game.state.game_finished and not initial:
            self.bend_button.config(state='disabled')
            self.result_label.config(text=random.choice(self.end_msgs), fg='purple')

    def quit_game(self):
        """退出游戏时保存进度并关闭窗口"""
        self.game.state.save()
        self.master.quit()

def main():
    root = tk.Tk()
    gui = SpoonGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()