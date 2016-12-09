#coding:utf-8
__author__ = "chenghao"

import pyorient
import util
from util import config

conf = config.Config()
conn = pyorient.OrientDB(conf.get("orientdb", "host"), conf.getint("orientdb", "port"))
conn.connect(conf.get("orientdb", "user"), conf.get("orientdb", "pwd"))


if conn.db_exists(util.DB_NAME):
	conn.db_open(util.DB_NAME, conf.get("orientdb", "user"), conf.get("orientdb", "pwd"))