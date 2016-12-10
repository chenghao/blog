# coding:utf-8
__author__ = "chenghao"

from bottle import request
import util


def get_user_id():
	"""
	获取user_id
	:return:
	"""
	cookie_id = request.get_cookie(util.BLOG_COOKIE)
	dogpile_session = util.GetDogpile()[1]
	result = dogpile_session.get(cookie_id)
	if result:
		user_id = result.get("rid")
	else:
		user_id = None
	return user_id
