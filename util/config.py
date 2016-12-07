# coding:utf-8
__author__ = "chenghao"

import ConfigParser

path = "../blog.ini"


class Singleton(type):
	def __init__(cls, name, bases, dict):
		super(Singleton, cls).__init__(name, bases, dict)
		cls._instances = None

	def __call__(cls, *args, **kwargs):
		if cls._instances is None:
			super(Singleton, cls).__call__(*args, **kwargs)
			cls._instances = ConfigParser.ConfigParser()
			cls._instances.read(path)
		return cls._instances


class Config(object):
	__metaclass__ = Singleton


if __name__ == "__main__":
	conf = Config()
	print(conf.get("orientdb", "user"))
	conf2 = Config()
	print(conf2.get("orientdb", "pwd"))
