# spoon_game.py
import time
import random
from config import SPOON_PROBABILITIES, TOTAL_SPOON_TYPES, SPOONS_PER_TYPE, MIN_ACTION_INTERVAL, SPOON_NAMES
from game_state import GameState
import os

class SpoonGame:
    def __init__(self):
        self.state = GameState()
        self.state.load()
        self.last_action_time = 0.0

        # 定义消息池
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

        # 从文件加载失败消息
        self.fail_msgs = self.load_fail_messages()

    def load_fail_messages(self):
        """从 fail_messages.txt 加载失败消息"""
        fail_messages = []
        fail_messages_file = os.path.join("message", "fail_messages.txt")
        try:
            with open(fail_messages_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        fail_messages.append(line)
            if not fail_messages:
                # 如果文件为空，使用默认消息
                fail_messages = [
                    "失败了，再接再厉！",
                    "还需要再多试几次！",
                    "别灰心，下次一定行！"
                ]
        except FileNotFoundError:
            # 如果文件不存在，使用默认消息
            fail_messages = [
                "失败了，再接再厉！",
                "还需要再多试几次！",
                "别灰心，下次一定行！"
            ]
        except Exception as e:
            # 其他异常，使用默认消息
            fail_messages = [
                "失败了，再接再厉！",
                "还需要再多试几次！",
                "别灰心，下次一定行！"
            ]
        return fail_messages

    def get_success_probability(self, spoon_type):
        return SPOON_PROBABILITIES.get(spoon_type, 1/10000)

    def try_bend_spoon(self):
        """尝试掰弯勺子的操作"""
        # 判断是否游戏已结束
        if self.state.game_finished:
            return "游戏已经结束！"

        # 间隔时间检查
        current_time = time.time()
        if current_time - self.last_action_time < MIN_ACTION_INTERVAL:
            return random.choice(self.too_fast_msgs)

        self.last_action_time = current_time

        # 计算概率
        p = self.get_success_probability(self.state.current_type)
        rnd = random.random()
        if rnd < p:
            # 成功掰断
            self.state.current_count += 1
            # 更新已掰弯的勺子计数
            self.state.bent_spoons[str(self.state.current_type)] = self.state.bent_spoons.get(str(self.state.current_type), 0) + 1
            result = f"成功掰断第 {self.state.current_type} 种勺子的第 {self.state.current_count} 根！"

            # 检查是否该切换下一个种类
            if self.state.current_count >= SPOONS_PER_TYPE:
                if self.state.current_type == TOTAL_SPOON_TYPES:
                    # 游戏结束
                    self.state.game_finished = True
                    result += "\n恭喜！你已经掰断了第十种勺子的第十根，游戏结束！"
                else:
                    self.state.current_type += 1
                    self.state.current_count = 0
                    result += f"\n切换到第 {self.state.current_type} 种勺子进行掰弯挑战！"
            self.state.save()
            return result
        else:
            # 未成功
            return random.choice(self.fail_msgs)

    def get_status(self):
        """获取当前游戏状态的描述"""
        if self.state.game_finished:
            return "游戏已完成！"
        else:
            spoon_name = SPOON_NAMES.get(self.state.current_type, f"第 {self.state.current_type} 种勺子")
            return f"当前勺子类型：{spoon_name} (种类 {self.state.current_type}), 已掰弯数量：{self.state.current_count}/{SPOONS_PER_TYPE}"