# -*- coding: utf-8 -*-
# Player-side

import hashlib
import inspect

def commit_function(func):
    """
    函數承諾（Function Commitment）
    對函數原始碼做雜湊 形成承諾
    確保抽卡使用的函數不會變
    """
    source = inspect.getsource(func)
    if isinstance(source, unicode):
        source = source.encode("utf-8")
    return hashlib.sha256(source).hexdigest()
