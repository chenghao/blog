#coding:utf-8
__author__ = "chenghao"

from bottle import Bottle
import util
from handler.blog import blog_app
from handler.admin import admin_app
from ueditor.ueditor import ueditor_bottle

Routes = Bottle()

# App to render / (home)
Routes.merge(blog_app)
# Mount other applications
Routes.mount(util.ADMIN_PREFIX, admin_app)
Routes.mount(util.UEDITOR_PREFIX, ueditor_bottle)