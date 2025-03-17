# game_state.py
import json
import os
from config import SAVE_FILE

class GameState:
    def __init__(self):
        self.current_type = 1         # 当前勺子种类(1~10)
        self.current_count = 0        # 当前种类已掰断勺子计数
        self.game_finished = False
        self.bent_spoons = {}         # 已掰弯的勺子数量，格式：{ "1": 3, "2": 5, ... }

    def load(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.current_type = data.get('current_type', 1)
                self.current_count = data.get('current_count', 0)
                self.game_finished = data.get('game_finished', False)
                self.bent_spoons = data.get('bent_spoons', {})
        else:
            # 无进度文件，从初始状态开始
            self.current_type = 1
            self.current_count = 0
            self.game_finished = False
            self.bent_spoons = {}

    def save(self):
        data = {
            'current_type': self.current_type,
            'current_count': self.current_count,
            'game_finished': self.game_finished,
            'bent_spoons': self.bent_spoons
        }
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)