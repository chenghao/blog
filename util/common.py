# coding:utf-8
__author__ = "chenghao"

from datetime import datetime, date
import re, uuid, json
import conf


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
	return uuid.uuid4().hex


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


def total_page(total_rows, rows=conf.rows):
	"""
	将总行数计算出多少页
	"""
	return int((total_rows - 1) / rows + 1)
