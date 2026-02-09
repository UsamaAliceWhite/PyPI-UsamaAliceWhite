# Copyright 2026 UsamaAliceWhite All Rights Reserved


# 標準モジュール
import dataclasses
import datetime
import logging
import logging.handlers
import pathlib

# 自作モジュール
from ..Shared import SingletonPattern


# --- ハンドラ機能 ---
# Parameter
@dataclasses.dataclass
class HandlerParameter:
    file_path: pathlib.Path = pathlib.Path.home() / "Logs/Unknown.log"
    when: str = "midnight"
    interval: int = 1
    backupcount: int = 99
    encoding: str | None = "utf-8"
    delay: bool = False
    utc: bool = False
    attime: datetime.time | None = None
    errors: str | None = None
    level: int = logging.DEBUG
    message_format: str = \
        "%(asctime)s [%(levelname)-8s] %(name)-15s %(funcName)s:%(lineno)d - %(message)s"
    datetime_format: str = "%Y-%m-%d %H:%M:%S"

# MainLogic
class HandlerManager(metaclass= SingletonPattern):
    # インスタンスの初期化
    def __init__(self, parameter: HandlerParameter) -> None:
        self.parameter: HandlerParameter = parameter
        self.handler: logging.handlers.TimedRotatingFileHandler | None = None
    
    # ディレクトリの作成
    def create_directory(self) -> None:
        try:
            directory_path: pathlib.Path = self.parameter.file_path.parent
            directory_path.mkdir(parents= True, exist_ok= True)
        except Exception as e:
            raise RuntimeError("Failed to create log file directory.") from e

    # ハンドラの作成及び設定
    def create_handler(self) -> logging.handlers.TimedRotatingFileHandler:
        if self.handler is None:
            try:
                handler: logging.handlers.TimedRotatingFileHandler = \
                    logging.handlers.TimedRotatingFileHandler(
                        filename= str(self.parameter.file_path),
                        when= self.parameter.when,
                        interval= self.parameter.interval,
                        backupCount= self.parameter.backupcount,
                        encoding= self.parameter.encoding,
                        delay= self.parameter.delay,
                        utc= self.parameter.utc,
                        atTime= self.parameter.attime,
                        errors= self.parameter.errors
                    )
                handler.setLevel(self.parameter.level)
                handler.setFormatter(logging.Formatter(
                    fmt= self.parameter.message_format,
                    datefmt= self.parameter.datetime_format
                ))
            except Exception as e:
                raise RuntimeError("Failed to create log handler.") from e
        
            self.handler = handler

        return self.handler            