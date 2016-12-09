#coding:utf-8
__author__ = "chenghao"

from bottle import Bottle, request, redirect, response, JSONPlugin
from json import dumps
import util
from util import encrypt
from dal import admin_dal

admin_app = Bottle()
admin_app.install(JSONPlugin(json_dumps=lambda s: dumps(s, cls=util.ComplexEncoder)))


@admin_app.post("/login")
def login():
	"""
	管理用户登录
	:return:
	"""
	login_name = request.params.getunicode("login_name")
	login_pwd = request.params.getunicode("login_pwd")
	result = admin_dal.login(login_name, login_pwd)


