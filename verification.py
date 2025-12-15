# -*- coding: utf-8 -*-
# Verifier-side

import math
from randomness import public_randomness_beacon
from lootbox import lootbox_function, PUBLIC_PROBABILITY

def run_trials(n):
    result = {"SSR": 0, "SR": 0, "R": 0}

    for i in range(n):
        rand = public_randomness_beacon(i)
        rarity = lootbox_function(rand)
        result[rarity] += 1

    return result

def z_test(observed, n, claimed):
    """
    z值是用來量化「實際結果和理論機率差多遠」的指標
    實際機率p_hat v.s. 宣稱機率claimed
    """
    p_hat = float(observed) / n                 # 實際機率
    se = math.sqrt(claimed * (1 - claimed) / n) # 標準誤差
    return (p_hat - claimed) / se               # z值 [z=(實際結果-理論期望)/正常的誤差範圍]

def verify_probability(n=100000):
    results = run_trials(n)

    for rarity in ["SSR", "SR"]:
        z = z_test(results[rarity], n, PUBLIC_PROBABILITY[rarity])
        
        # 使用統計學的門檻值 
        # 在常態分布（鐘形曲線）中 z值範圍在−1.96～+1.96是95%的正常情況
        if z < -1.96:
            print "{} X The probability is lower than the claimed value.".format(rarity)
        elif z > +1.96:
            print "{} X The probability is higher than the claimed value.".format(rarity)
        else:
            print "{} O Pass".format(rarity)
