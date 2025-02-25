'''
Author: lvmiaochun
Date: 2024-10-25
'''
import logging.config
import codecs
from os import path


class Logger:

    def __init__(self):
        log_file_path = path.join(path.dirname(path.abspath(__file__)), '../config/log.conf')
        # 将disable_existing_loggers设置为FALSE避免将原有的logger禁用
        # 【2025/1/5 debug】指定以UTF-8编码读取配置文件
        with codecs.open(log_file_path, 'r', encoding='UTF-8') as f:
            logging.config.fileConfig(f, disable_existing_loggers=0)
        # logging.config.fileConfig(log_file_path, disable_existing_loggers=0)

        self.logger = logging.getLogger(__name__)

    @staticmethod
    def info(message):
        Logger().logger.info(message)

    @staticmethod
    def debug(message):
        Logger().logger.debug(message)

    @staticmethod
    def warning(message):
        Logger().logger.warning(message)

    @staticmethod
    def error(message):
        Logger().logger.error(message)
