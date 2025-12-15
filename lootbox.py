# -*- coding: utf-8 -*-
# Game-side

# 公開機率
PUBLIC_PROBABILITY = {
    "SSR": 0.01,
    "SR":  0.09,
    "R":   0.90
}

# 遊戲實際使用機率
_PROBABILITY = {
    "SSR": 0.01,
    "SR":  0.09,
    "R":   0.90
}

def lootbox_function(rand_value):
    """
    轉蛋函數（商業機密）
    """
    if rand_value < _PROBABILITY["SSR"]:
        return "SSR"
    elif rand_value < _PROBABILITY["SSR"] + _PROBABILITY["SR"]:
        return "SR"
    else:
        return "R"

__all__ = ["lootbox_function", "PUBLIC_PROBABILITY"]