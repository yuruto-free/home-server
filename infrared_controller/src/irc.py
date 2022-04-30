#!/usr/bin/python3
# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from adrsirlib import Adrsir
import threading
import json
import logging
import logging.config
import os
import signal
import time

class InfraredController():
    """
    赤外線コントローラ

    Attributes
    ----------
    __logger : logging
        logger
    __ir : Adrsir
        赤外線操作ライブラリ
    __commands : dict of dict
        対象機器ごとのコマンド
    """

    def __init__(self, log_configure, config_name):
        """
        コンストラクタ

        Parameters
        ----------
        log_configure : dict
            logging情報
        config_name : str
            config名
        """
        # logger
        logging.config.dictConfig(log_configure)
        self.__logger = logging.getLogger(config_name)
        # ADRSIRライブラリ
        self.__ir = Adrsir()
        # コマンドリスト
        self.__commands = {}

    def initialize(self, root_dir, json_config_path):
        """
        initialize

        Parameters
        ----------
        root_dir : str
            root directory
        json_config_path : str
            JSON configファイルパス
        """
        self.__logger.info('Start initialization')

        # configファイルの読み込み
        try:
            with open(json_config_path, 'r') as fin:
                config = json.load(fin)
            # コマンドデータの読み込み
            for machine_name, json_file_path in config.items():
                with open(os.path.join(root_dir, json_file_path), 'r') as fin:
                    self.__commands[machine_name] = json.load(fin)
        except Exception as e:
            self.__logger.warning('Error: Json file cannot read.')
            raise Exception(e)

        self.__logger.info('Complete initialization')

    def logging_error(self, err_msg):
        """
        logging error message

        Parameters
        ----------
        err_msg : str
            エラーメッセージ
        """
        self.__logger.warning(err_msg)

    def finalize(self):
        """
        finalize
        """
        self.__logger.info('Stop {}'.format(self.__class__.__name__))

    def execute(self, event):
        """
        実行

        Parameters
        ----------
        event : json string
            machine : 機器の名称（JSON_CONFIG_PATH内で定義されているkey）
            command : 実行対象のコマンドリスト
            message : 処理内容

        Returns
        -------
        response : json string
            status_code : ステータスコード
            message : 処理内容 or エラーメッセージ
        """

        try:
            # 情報を取得
            data = json.loads(event)
            machine = data['machine']
            command = data['command']
            message = data['message']

            # コマンド取得
            send_cmd = self.__commands[machine][command]
            # コマンド送信
            if isinstance(send_cmd, str):
                self.__ir.send(send_cmd)
            elif isinstance(send_cmd, (list, tuple)):
                for cmd in send_cmd:
                    self.__ir.send(cmd)
                    time.sleep(0.5)
            else:
                raise Exception('command type error')
            self.__logger.info(message)
            response = {'status_code': 200, 'message': message}
        except Exception as e:
            self.__logger.warning('Invalid data ({})'.format(e))
            raise Exception(e)

        return response

class CallbackServer(BaseHTTPRequestHandler):
    """
    HTTPのリクエストとレスポンスを処理する

    Attributes
    ----------
    __callback : callable object
        コールバック関数
    """

    def __init__(self, callback, *args):
        """
        コンストラクタ

        Parameters
        ----------
        callback : callable object
            コールバック関数
        *args : tuple
            可変長引数
        """
        self.__callback = callback
        super().__init__(*args)

    def do_POST(self):
        """
        POSTに対する処理
        """
        try:
            content_length = int(self.headers.get('content-length'))
            request = self.rfile.read(content_length).decode('utf-8')
            response = self.__callback(request)
        except Exception as e:
            response = {'status_code': 500, 'message': e}

        self.send_response(response['status_code'])
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

class HttpServer(threading.Thread):
    """
    HTTPサーバ

    Attributes
    ----------
    __port : int
        ポート番号
    __callback : callable object
        コールバック関数
    """

    def __init__(self, port, callback):
        """
        コンストラクタ

        Parameters
        ----------
        port : int
            ポート番号
        callback : callable object
            コールバック関数
        """
        super().__init__()
        self.__port = port
        self.__callback = callback

    def run(self):
        """
        スレッド実行時に呼び出される関数
        """
        def handler(*args):
            CallbackServer(self.__callback, *args)
        self.server = ThreadingHTTPServer(('', self.__port), handler)
        self.server.serve_forever()

    def stop(self):
        """
        スレッド終了時に呼び出す関数
        """
        self.server.shutdown()
        self.server.server_close()

class ProcessStatus():
    """
    プロセスの状態

    Attributes
    ----------
    __status : bool
        True  : 実行中
        False : 停止中
    """

    def __init__(self):
        """
        コンストラクタ
        """
        self.__status = True

    def change_status(self, signum, frame):
        """
        ステータスの変更

        Parameters
        ----------
        signum : int
            シグナル番号
        frame : str
            フレーム情報
        """
        self.__status = False

    def get_status(self):
        """
        現在のステータスの取得
        """
        return self.__status

# ================
# = main routine =
# ================
if __name__ == '__main__':
    # ========
    # 定数定義
    # ========
    config_name = 'irc'
    root_dir = os.getenv('APP_ROOT_PATH', '/infrared_controller')
    json_config_path = os.path.join(root_dir, 'config.json')
    log_absolute_path = '/var/log/{}.log'.format(config_name)
    http_port = int(os.getenv('HTTP_PORT', '8180'))

    # ===============
    # logのconfig設定
    # ===============
    log_configure = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'infoFormat': {
                'format': '[%(asctime)s %(levelname)s] %(name)s %(message)s',
                'datefmt': '%Y/%m/%d %H:%M:%S'
            }
        },
        'handlers': {
            'timeRotate': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'infoFormat',
                'filename': log_absolute_path,
                'when': 'W2',
                'backupCount': 5
            },
            'consoleHandler': {
                'class': 'logging.StreamHandler',
                'formatter': 'infoFormat'
            }
        },
        'loggers': {
            config_name: {
                'level': 'INFO',
                'handlers': ['timeRotate', 'consoleHandler']
            }
        }
    }

    # ================================
    # プロセス監視用インスタンスの生成
    # ================================
    process_status = ProcessStatus()
    signal.signal(signal.SIGINT, process_status.change_status)
    signal.signal(signal.SIGTERM, process_status.change_status)

    # ============================
    # 赤外線制御用インスタンス生成
    # ============================
    ic = InfraredController(log_configure, config_name)

    try:
        # ==========
        # initialize
        # ==========
        ic.initialize(root_dir, json_config_path)

        # ============================
        # HTTPサーバのインスタンス生成
        # ============================
        server = HttpServer(http_port, ic.execute)

        # =============
        # = main loop =
        # =============
        server.start()
        while process_status.get_status():
            time.sleep(0.1)
        server.stop()

    except Exception as e:
        ic.logging_error('Error(main): {}'.format(e))
    # ========
    # finalize
    # ========
    ic.finalize()
