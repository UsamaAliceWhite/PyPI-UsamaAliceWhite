# Copyright 2026 UsamaAliceWhite All Rights Reserved


# 標準モジュール
import dataclasses
import logging
import logging.handlers
import threading


# --- ロガー機能 ---
# Parameter
@dataclasses.dataclass
class LoggerParameter:
    handler: logging.handlers.TimedRotatingFileHandler
    name: str = "Unknown"
    level: int = logging.DEBUG

# MainLogic
class LoggerManager:
    _lock: threading.Lock = threading.Lock()

    # インスタンスの初期化
    def __init__(self, parameter: LoggerParameter) -> None:
        self.parameter: LoggerParameter = parameter
    
    # ロガーの作成及び設定
    def create_logger(self) -> logging.Logger:
        try:
            with LoggerManager._lock:
                logger: logging.Logger = logging.getLogger(self.parameter.name)
                if self.parameter.handler not in logger.handlers:
                    logger.setLevel(self.parameter.level)
                    logger.addHandler(self.parameter.handler)
                    logger.propagate = False
        except Exception as e:
            raise RuntimeError("Failed to create logger.") from e
        
        return logger