#coding:utf-8
__author__ = "chenghao"

import util, dal
conn = dal.conn


def create_db(db_name=util.DB_NAME):
	"""
	检查数据库，如果不存在则创建
	:param db_name:
	:return:
	"""
	if not conn.db_exists(db_name):
		conn.db_create(db_name)


def create_table():
	"""
	创建表
	:return:
	"""
	table_name = ["user", "category", "article"]
	for table in table_name:
		sql = "create class %s" % table
		conn.command(sql)


if __name__ == "__main__":
	create_db()
	create_table()