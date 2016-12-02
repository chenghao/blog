# coding:utf-8
__author__ = "chenghao"

import ConfigParser


class Config:
	def __init__(self, path="../blog.ini"):
		self.path = path
		self.cf = ConfigParser.ConfigParser()
		self.cf.read(self.path)

	def get(self, field, key):
		result = ""
		try:
			result = self.cf.get(field, key)
		except:
			result = ""
		return result

if __name__ == "__main__":
	conf = Config()
	print(conf.get("cassandra", "user"))
	print(conf.get("cassandra", "pwd"))