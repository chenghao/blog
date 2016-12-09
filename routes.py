#coding:utf-8
__author__ = "chenghao"

from bottle import Bottle
import util
from handler.blog import blog_app
from handler.admin import admin_app
from ueditor.ueditor import ueditor_bottle

Routes = Bottle()

# 主路径（默认）
Routes.merge(blog_app)
# 挂载其它模块路径
Routes.mount(util.ADMIN_PREFIX, admin_app)
Routes.mount(util.UEDITOR_PREFIX, ueditor_bottle)