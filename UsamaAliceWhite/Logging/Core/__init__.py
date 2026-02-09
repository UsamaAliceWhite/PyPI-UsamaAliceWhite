# Copyright 2026 UsamaAliceWhite All Rights Reserved


# 標準モジュール
import datetime
import logging
import logging.handlers
import pathlib

# 自作モジュール
from .Handler import HandlerManager, HandlerParameter
from .Logger import LoggerManager, LoggerParameter


# 公開API
__all__ = ["GetLogger"]


# --- ロギング機能 ---
class GetLogger:
    """
    引数:
        logger_name:
            ロガー名。
            __name__を推奨。
        logger_level:
            ログレベル。
            - logging.DEBUG    : 10
            - logging.INFO     : 20
            - logging.WARNING  : 30
            - logging.ERROR    : 40
            - logging.CRITICAL : 50
        log_file_path:
            ログファイルの保存先パス。
            初期値はホームディレクトリに展開。
        log_message_format:
            ログの出力形式。
            - %(asctime)s   : 日時
            - %(name)s      : ロガー名
            - %(levelname)s : ログレベル
            - %(message)s   : ログメッセージ
            - %(filename)s  : ファイル名
            - %(lineno)d    : 行番号
            - %(funcName)s  : 関数名
        log_datetime_format:
            ログの日時の出力形式。
        handler_when:
            ログファイルのローテーションの間隔。
            - "S"         : 秒
            - "M"         : 分
            - "H"         : 時
            - "D"         : 日
            - "midnight"  : 00時00分
            - "W0" - "W6" : 曜日（W0=月曜日,W6=日曜日）
        handler_interval:
            ログファイルのローテーションの頻度。
            （1=毎回,5=5回に1度:when="D"+interval=5の場合、5日に1度）
        handler_backupcount:
            保持するバックアップファイルの上限数。
        handler_encoding:
            ログファイルの文字コード。
            （"utf-8","shift-jis"など）
        handler_delay:
            ログファイルの作成タイミングを遅らせる設定。
            - True  : 初回のログ出力時にログファイルを作成。
            - False : GetLoggerの初回の実行時に作成。
        handler_utc:
            日時の基準。
            - True  : 世界標準時
            - False : ローカル時刻（日本の場合、JST）
        handler_attime:
            ローテーションを実行する時刻。
            （when="midnight"+attime=datetime.time(2,15)の場合、毎日2時15分に実行）
        handler_errors:
            ファイル書き込み時の文字コードに関するエラー対処。
            指定した文字コードに対応していない文字が出現した場合に出力される文字。
    返値:
        設定済みのロガー。
    詳細:
        初回にログハンドラとロガーを作成。
        2回目以降は初回に作成したログハンドラと再利用しロガーを作成。
        ただし、作成済みのロガーと同名である場合はロガーを再利用。
        シングルトンパターンによりアプリケーション全体で同じハンドラを共有。
    """
    # ロガーの取得
    def __new__(cls,
                logger_name: str = "Unknown",
                logger_level: int = logging.DEBUG,
                *,
                log_file_path: pathlib.Path | str = pathlib.Path.home() / "Logs/Unknown.log",
                log_message_format: str = \
                    "%(asctime)s [%(levelname)-8s] %(name)-15s %(funcName)s:%(lineno)d - %(message)s",
                log_datetime_format: str = "%Y-%m-%d %H:%M:%S",
                handler_when: str = "midnight",
                handler_interval: int = 1,
                handler_backupcount: int = 99,
                handler_encoding: str | None = "utf-8",
                handler_delay: bool = False,
                handler_utc: bool = False,
                handler_attime: datetime.time | None = None,
                handler_errors: str | None = None,
                handler_level: int = logging.DEBUG
                ) -> logging.Logger:
        instance: GetLogger = super().__new__(cls)
        handler_parameter: HandlerParameter = HandlerParameter(
            file_path= pathlib.Path(log_file_path),
            when= handler_when,
            interval= handler_interval,
            backupcount= handler_backupcount,
            encoding= handler_encoding,
            delay= handler_delay,
            utc= handler_utc,
            attime= handler_attime,
            errors= handler_errors,
            level= handler_level,
            message_format= log_message_format,
            datetime_format= log_datetime_format
        )
        handler: logging.handlers.TimedRotatingFileHandler = \
            instance._get_handler(parameter= handler_parameter)
        logger_parameter: LoggerParameter = LoggerParameter(
            handler= handler,
            name= logger_name,
            level= logger_level
        )
        logger: logging.Logger = instance._get_logger(parameter= logger_parameter)

        return logger
    
    # ハンドラの取得
    def _get_handler(self, parameter: HandlerParameter) -> logging.handlers.TimedRotatingFileHandler:
        manager: HandlerManager = HandlerManager(parameter= parameter)
        manager.create_directory()
        handler: logging.handlers.TimedRotatingFileHandler = manager.create_handler()
        
        return handler
    
    # ロガーの取得
    def _get_logger(self, parameter: LoggerParameter) -> logging.Logger:
        manager: LoggerManager = LoggerManager(parameter= parameter)
        logger: logging.Logger = manager.create_logger()

        return logger
