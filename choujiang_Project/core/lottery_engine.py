# core/lottery_engine.py

import random

def contains_digit_4(n: int) -> bool:
    return '4' in str(n)


class LotteryEngine:
    MIN_GAP = 3  # 邻号最小间隔

    def __init__(self):
        self.start = 1
        self.end = 100
        self.prizes = []
        self.used_numbers = set()
        self.prize_drawn = {}
        self.valid_numbers = []

    def set_settings(self, start, end, prizes):
        self.start = start
        self.end = end
        self.prizes = prizes
        self.used_numbers.clear()
        self.prize_drawn = {p["name"]: [] for p in prizes}

        # 生成不含数字4的号码池
        self.valid_numbers = [
            n for n in range(start, end + 1)
            if not contains_digit_4(n)
        ]

        # 检查号码是否足够
        total_needed = sum(p["count"] for p in prizes)
        if len(self.valid_numbers) < total_needed:
            raise ValueError(
                f"可用号码不足！范围 [{start}, {end}] 中不含4的号码共 {len(self.valid_numbers)} 个，"
                f"但奖项总共需要 {total_needed} 个。"
            )

    def _is_too_close(self, num):
        """检查号码是否与已抽出的号码间隔小于5"""
        for used in self.used_numbers:
            if abs(num - used) < self.MIN_GAP:
                return True
        return False

    def draw_once(self, prize_name):
        prize_info = next((p for p in self.prizes if p["name"] == prize_name), None)
        if not prize_info:
            raise ValueError(f"未知奖项：{prize_name}")

        drawn = self.prize_drawn[prize_name]
        if len(drawn) >= prize_info["count"]:
            return None

        # 排除已使用的号码
        available = [n for n in self.valid_numbers if n not in self.used_numbers]
        if not available:
            raise RuntimeError("所有不含4的号码已抽完！")

        # 优先选择间隔>=5的号码
        safe_numbers = [n for n in available if not self._is_too_close(n)]
        
        # 如果没有安全号码，退而求其次使用所有可用号码
        pool = safe_numbers if safe_numbers else available
        
        winner = random.choice(pool)
        self.used_numbers.add(winner)
        drawn.append(winner)
        return winner