# coding:utf-8
__author__ = "chenghao"

import hashlib, base64


def get_md5_s(s):
	secret_s = "5*j,.^&;?.%#@!"
	if s == "":
		return ""
	md5code = hashlib.md5(s.encode()).hexdigest()[8:10]
	key = hashlib.md5(secret_s.encode()).hexdigest()
	len_key = len(key)
	code = ""
	for i in range(len(s)):
		k = i % len_key
		# 先转为ascii在进行 ^ 运算
		_s = ord(s[i])
		_key = ord(key[k])

		code += str(_s ^ _key)

	_encode = base64.b64encode(code.encode("utf8"))
	code = _encode.decode() + md5code

	return code

if __name__ == "__main__":
	print(get_md5_s("chenghao"))
	print(get_md5_s("hao"))