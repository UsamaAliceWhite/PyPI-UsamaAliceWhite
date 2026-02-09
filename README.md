## ------ ロギング機能 ------
### 説明
「アプリケーション全体でログを一元管理する。簡単にログを出力できる。」  
これらをコンセプトとしている。  

本機能はアプリ全体で一つの設定を共有する。  
その為、最初にGetLoggerを呼び出した際の設定がアプリ終了時まで全てのロガーに適応される。  

### 関数
GetLogger()  
- ログハンドラの設定とロガーの取得を行う。
- 初期値は「毎日00時00分にログファイルをローテーションする。過去のログファイルは99ファイルまで保管される。」

### サンプルコード
```
from UsamaAliceWhite.Logging import GetLogger  
logger = GetLogger(logger_name= __name__)
logger.info("usama alice white")
```

## ------ ディレクトリ構造 ------
```
UsamaAliceWhite_Ver1.0.0/
├── UsamaAliceWhite/
│   ├── Logging/
│   │   ├── Core/
│   │   │   ├── __init__.py
│   │   │   ├── Handler.py
│   │   │   └── Logger.py
│   │   ├── Shared/
│   │   │   ├── __init__.py
│   │   │   └── Singleton.py
│   │   └── __init__.py
│   ├── __init__.py
│   └── py.typed
├── pyproject.toml
└── README.md
```