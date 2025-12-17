# -*- coding: utf-8 -*-
# Verifier-side

import math, hashlib, os
from randomness import public_randomness_beacon
from lootbox import lootbox_function, PUBLIC_PROBABILITY
from commitment import verify_hash_chain

def verify_opening(rand_value, rarity, proof):
    """
    Verify π = H(x || y)
    """
    data = "{}|{}".format(rand_value, rarity)
    expected = hashlib.sha256(data).hexdigest()
    return expected == proof

def generate_hash_chain(n):
    """
    Generate hash chain:
    s_n -> s_{n-1} -> ... -> s_0
    Publish h_0 = H(s_0)
    """
    hashes = []

    s = os.urandom(16).encode("hex")
    for i in range(n):
        h = hashlib.sha256(s).hexdigest()
        hashes.append(h)
        s = h

    # 公開最後一個 hash 作為承諾
    last_hash = hashes.pop()
    
    return last_hash, hashes

def run_trials(n, last_hash, hashes):
    result = {"SSR": 0, "SR": 0, "R": 0}

    for i in range(n):
        if not verify_hash_chain(last_hash, hashes[-1]):
            raise Exception("Hash chain verification failed")

        prb = public_randomness_beacon(i)
        combined = float(int(last_hash, 16)) / (2**256)
        rand_input = (combined + prb) % 1.0
        rarity, proof = lootbox_function(rand_input)
        result[rarity] += 1

        if not verify_opening(rand_input, rarity, proof):
            raise Exception("Invalid opening proof")

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
    last_hash, hashes = generate_hash_chain(n)
    results = run_trials(n, last_hash, hashes)

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
