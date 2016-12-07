# coding:utf-8
__author__ = "chenghao"

import pyorient

conn = pyorient.OrientDB("localhost", 2424)
conn.connect("root", "123456")


def check_database(database_name):
	"""
	检查数据库，如果不存在则创建
	:param database_name:
	:return:
	"""
	if conn.db_exists(database_name):
		conn.db_open(database_name, "root", "123456")
	else:
		conn.db_create(database_name)


def create_table():
	"""
	创建表
	:return:
	"""
	table_name = ["user", "category", "article"]
	for table in table_name:
		sql_table = "create class %s" % table
		command(sql_table)


def command(sql):
	return conn.command(sql)


def query(sql):
	return conn.query(sql)


def init_db():
	check_database("blog") # 创建数据库
	create_table() # 创建数据表


if __name__ == "__main__":
	# init_db()

	#####################################################
	check_database("blog")

	sql = "insert into category set title='python'"  #新增数据
	# result = command(sql)
	# print result[0]._rid # 获取主键

	sql = "update category set title='python2' where @rid=#25:3"  # 修改数据
	# print command(sql)

	sql = "delete from category where @rid=#25:3"  # 删除数据
	# print command(sql)

	sql = "select from category"  # 查询数据
	result = query(sql)
	for r in result:
		print type(r), r
		print r._rid, r.title

