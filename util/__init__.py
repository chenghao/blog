# coding:utf-8
__author__ = "chenghao"

from util import config
import os, logging, re, uuid, json
from logging import handlers
from datetime import datetime, date

ADMIN_PREFIX = "/admin"
UEDITOR_PREFIX = "/ueditor"


def get_rows():
	"""
	获取每页显示行数
	:return:
	"""
	conf = config.Config()
	return conf.getint("basic", "rows")


def get_current_date(pattern="%Y-%m-%d %H:%M:%S", datetime_s=None):
	"""
	格式化日期
	:param pattern:
	:param datetime_s:
	:return:
	"""
	if datetime_s is None:
		result = datetime.now().strftime(pattern)
	elif isinstance(datetime_s, datetime):
		result = datetime_s.strftime(pattern)
	elif isinstance(datetime_s, date):
		result = datetime_s.strftime("%Y-%m-%d")
	else:
		result = datetime_s
	return result


def ver_mobile(data):
	"""
	验证手机号，正确返回True
	:param data:
	:return:
	"""
	p = re.compile(r"((13|14|15|17|18)\d{9}$)")
	return p.match(data)


def ver_email(data):
	"""
	验证邮箱，正确返回True
	:param data:
	:return:
	"""
	p = re.compile(r"(\w+[@]\w+[.]\w+)")
	return p.match(data)


def random_num():
	"""
	获取随机数
	:return:
	"""
	return uuid.uuid4().hex.lower()


class ComplexEncoder(json.JSONEncoder):
	"""
	json日期格式化
	"""

	def default(self, obj):
		if isinstance(obj, datetime):
			return obj.strftime('%Y-%m-%d %H:%M:%S')
		elif isinstance(obj, date):
			return obj.strftime('%Y-%m-%d')
		else:
			return json.JSONEncoder.default(self, obj)


def total_page(total_rows, rows=None):
	"""
	将总行数计算出多少页
	"""
	if rows is None:
		rows = get_rows()
	return int((total_rows - 1) / rows + 1)


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
	print total_page(24)
