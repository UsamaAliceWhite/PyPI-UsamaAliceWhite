# Copyright 2026 UsamaAliceWhite All Rights Reserved


# 標準モジュール
import threading
import typing


# --- シングルトンパターン ---
class SingletonPattern(type):
    _instance: dict[type, typing.Any] = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        if cls not in cls._instance:
            with cls._lock:
                if cls not in cls._instance:
                    instance: typing.Any = super().__call__(*args, **kwargs)
                    cls._instance[cls] = instance
        return cls._instance[cls]