#coding:utf-8
__author__ = "chenghao"

from bottle import Bottle, request, redirect, response, JSONPlugin
from json import dumps
import util

blog_app = Bottle()
blog_app.install(JSONPlugin(json_dumps=lambda s: dumps(s, cls=util.ComplexEncoder)))
