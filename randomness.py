# -*- coding: utf-8 -*-
# Verifier-side

import hashlib
import time

def public_randomness_beacon(seed):
    """
    公開亂數信標（Public Randomness Beacon）
    模擬公開、不可控制的亂數來源
    任何人都能算出結果，但遊戲方無法作弊
    """
    data = "{}-{}".format(seed, int(time.time()))
    digest = hashlib.sha256(data).hexdigest()
    return int(digest, 16) / float(2**256)
