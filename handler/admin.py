#coding:utf-8
__author__ = "chenghao"

from bottle import Bottle, request, redirect, response, JSONPlugin
from json import dumps
import util

admin_app = Bottle()
admin_app.install(JSONPlugin(json_dumps=lambda s: dumps(s, cls=util.ComplexEncoder)))
