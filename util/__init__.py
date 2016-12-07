#coding:utf-8
__author__ = "chenghao"

from util import config

ADMIN_PREFIX = "/admin"
UEDITOR_PREFIX = "/ueditor"


def get_rows():
	"""
	获取每页显示行数
	:return:
	"""
	conf = config.Config()
	return conf.get("basic", "rows")


if __name__ == "__main__":
	print get_rows()