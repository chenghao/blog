#coding:utf-8
__author__ = "chenghao"

from util import config
import os, logging
from logging import handlers


ADMIN_PREFIX = "/admin"
UEDITOR_PREFIX = "/ueditor"


def get_rows():
	"""
	获取每页显示行数
	:return:
	"""
	conf = config.Config()
	return conf.get("basic", "rows")


class SingletonLog(type):
	"""
	日志单例
	"""
	def __init__(cls, name, bases, dict):
		super(SingletonLog, cls).__init__(name, bases, dict)
		cls._instances = None

	def __call__(cls, *args, **kwargs):
		if cls._instances is None:
			super(SingletonLog, cls).__call__(*args, **kwargs)
			conf = config.Config()
			# 按每天生成日志文件 linux
			log_file_path = conf.get("log", "path")
			if not os.path.exists(log_file_path):
				os.makedirs(log_file_path)
			log_handler = handlers.TimedRotatingFileHandler(log_file_path + "/blog", conf.get("log", "when"),
															conf.getint("log", "interval"))
			# 格式化日志内容
			format_ = "%(asctime)s %(pathname)-5s %(funcName)-5s %(lineno)-5s %(levelname)-5s %(message)s"
			log_formatter = logging.Formatter(format_)
			log_handler.setFormatter(log_formatter)
			# 设置记录器名字
			log = logging.getLogger('blog')
			log.addHandler(log_handler)
			# 设置日志等级
			log.setLevel(conf.get("log", "level"))
			cls._instances = log
		return cls._instances


class GetLogging(object):
	"""
	获取log实例
	"""
	__metaclass__ = SingletonLog


if __name__ == "__main__":
	print get_rows()

	log = GetLogging()
	log.info("222222")