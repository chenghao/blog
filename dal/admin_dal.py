#coding:utf-8
__author__ = "chenghao"

from dal import conn
from util import encrypt


def login(login_name, login_pwd):
	sql = """
			select @rid as rid, user_name, login_name
			from user where login_name='%s' and login_pwd='%s'
		""" % (login_name, encrypt.get_md5_s(login_pwd))
	results = conn.query(sql)
	if len(results) > 0:
		return results[0].oRecordData
	else:
		return False


if __name__ == "__main__":
	result = login("chenghao", "13158460430")
	print result["rid"]