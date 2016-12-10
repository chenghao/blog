# coding:utf-8
__author__ = "chenghao"

from bottle import Bottle, request, redirect, response, JSONPlugin, jinja2_view as view
from json import dumps
import handler, util
from dal import admin_dal

admin_app = Bottle()
admin_app.install(JSONPlugin(json_dumps=lambda s: dumps(s, cls=util.ComplexEncoder)))


######################### 后台管理 #########################
@admin_app.get("/", apply=[view("./admin/index")])
def index():
	return {}



######################### 后台登录 #########################
@admin_app.get("/login", apply=[view("./admin/login")])
def login():
	"""
	显示登录页面, 如果已经登录就重定向到后台管理主页
	:return:
	"""
	rid = handler.get_user_id()
	if rid:
		redirect("/admin")
	else:
		return {}


@admin_app.post("/login")
def login():
	"""
	管理用户登录
	:return:
	"""
	login_name = request.params.getunicode("login_name")
	login_pwd = request.params.getunicode("login_pwd")
	result = admin_dal.login(login_name, login_pwd)
	if result:
		# 设置 cookie
		cookie_id = util.random_num()
		dogpile_session = util.GetDogpile()[1]
		dogpile_session.set(cookie_id, result)

		conf = util.config.Config()
		max_age = conf.getint("cookie", "max_age")
		path = conf.get("cookie", "path")
		response.set_cookie(util.BLOG_COOKIE, cookie_id, max_age=max_age, path=path)

		return {"code": 0}
	else:
		return {"code": -1, "msg": "用户名或密码错误"}