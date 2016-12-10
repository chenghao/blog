# coding:utf-8
__author__ = "chenghao"

from util import config
import os, logging, re, uuid, json
from logging import handlers
from datetime import datetime, date
from dogpile.cache import make_region

# 基本配置
ADMIN_PREFIX = "/admin"  # 管理平台访问前缀
UEDITOR_PREFIX = "/ueditor"  # 富文本编辑访问前缀
ROW = 10    # 每页显示多少行
DB_NAME = "blog"  # 数据库名称
BLOG_COOKIE = "blog.cookie"  # cookie


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


def total_page(total_rows, rows=ROW):
	"""
	将总行数计算出多少页
	"""
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


class SingletonDogpile(type):
	"""
	缓存单例
	"""
	def __init__(cls, name, bases, dict):
		super(SingletonDogpile, cls).__init__(name, bases, dict)
		cls._instances_cache = None
		cls._instances_session = None

	def __call__(cls, *args, **kwargs):
		if cls._instances_cache is None and cls._instances_session is None:
			super(SingletonDogpile, cls).__call__(*args, **kwargs)
			conf = config.Config()

			file_path = conf.get("dogpile", "cache.file.arguments.filename")
			parent_path = os.path.dirname(file_path)
			if not os.path.exists(parent_path):
				os.makedirs(parent_path)

			dogpile_conf = {
				"cache.memory.backend": conf.get("dogpile", "cache.memory.backend"),
				"cache.memory.expiration_time": conf.getint("dogpile", "cache.memory.expiration_time"),
				"cache.file.backend": conf.get("dogpile", "cache.file.backend"),
				"cache.file.expiration_time": conf.getint("dogpile", "cache.file.expiration_time"),
				"cache.file.arguments.filename": conf.get("dogpile", "cache.file.arguments.filename"),

				"session.memory.backend": conf.get("dogpile", "session.memory.backend"),
				"session.memory.expiration_time": conf.getint("dogpile", "session.memory.expiration_time"),
				"session.file.backend": conf.get("dogpile", "session.file.backend"),
				"session.file.expiration_time": conf.get("dogpile", "session.file.expiration_time"),
				"session.file.arguments.filename": conf.get("dogpile", "session.file.arguments.filename")
			}
			cls._instances_cache = make_region().configure_from_config(dogpile_conf, "cache.file.")
			cls._instances_session = make_region().configure_from_config(dogpile_conf, "session.file.")
		return cls._instances_cache, cls._instances_session


class GetDogpile(object):
	"""
	获取缓存实例
	"""
	__metaclass__ = SingletonDogpile


if __name__ == "__main__":
	print total_page(24)
	dogpiles = GetDogpile()
	dogpile_cache = dogpiles[1]
	dogpile_cache.set("chenghao", "222333444")
	print dogpile_cache.get("chenghao")
	dogpile_cache.delete("chenghao")
	print dogpile_cache.get("chenghao")
