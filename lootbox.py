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
    f(x) → (y, π)
    π = hash(x || y)
    """
    if rand_value < _PROBABILITY["SSR"]:
        rarity = "SSR"
    elif rand_value < _PROBABILITY["SSR"] + _PROBABILITY["SR"]:
        rarity = "SR"
    else:
        rarity = "R"

    proof = _generate_proof(rand_value, rarity)
    return rarity, proof

def _generate_proof(x, y):
    import hashlib
    data = "{}|{}".format(x, y)
    return hashlib.sha256(data).hexdigest()

__all__ = ["lootbox_function", "PUBLIC_PROBABILITY"]