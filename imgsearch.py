#!/usr/bin/emv python 3
# coding:utf-8

from urllib import request,parse
from json import dump,loads,load
from os import path,mkdir,remove		
import sys

API_NAME=''	# your account name
API_KEY=''	# your account key
DUMPFILE='result.json'

"""
Get imagefile from Bing search API
"""

class Search:
	def __init__(self):
		self.root="https://api.datamarket.azure.com/Bing/Search/"
		self.api_name=API_NAME
		self.api_key=API_KEY
		self.search_word=""

	def image(self,search_word="",num=50):
		self.search_word=search_word
		skip=0
		while num>0:
			params={
				'Query':"'{}'".format(search_word),
				'$format':'json',
				'$top':'{}'.format(num),
				'$skip':'{}'.format(skip)
				}
			self.search('Image?'+parse.urlencode(params))
			num-=50
			skip+=50

	def search(self,query):
		url=self.root+query
		
		# ドキュメントにあるauth_handler=request.HTTPBasicAuthHandler() を使ったら失敗した…代わりに、パスワードマネージャを生成して認証したら成功
		# passwordマネージャを生成
		pass_mgr=request.HTTPPasswordMgrWithDefaultRealm()
		pass_mgr.add_password(
			realm=None,
			uri=url,
			user= API_NAME,
			passwd=API_KEY
			)
		opener=request.build_opener(request.HTTPBasicAuthHandler(pass_mgr))
		request.install_opener(opener)

		response=request.urlopen(url)

		# urlopenで取得するのはバイトオブジェクト、自力でパース
		result= loads(response.read().decode('utf-8'))

		#self.save(result)
		self.img_get(result)

	def save(self,result):
		with open(DUMPFILE,'a') as f:
			dump(result,f,sort_keys=True,indent=4)

	# dictからurlを読み込んで画像を取得
	def img_get(self,dic):
		EXT={b'\xff\xd8':'.jpg',b'\x47\x49':'.gif',b'\x89\x50':'.png'}
		DIR="./{0}".format(self.search_word)

		if not path.isdir(DIR):
			mkdir(DIR)

		for key,item in enumerate(dic["d"]["results"]):
			try:
				res_bin=request.urlopen(item["MediaUrl"]).read()
				# ヘッダを読んで拡張子を決定
				ext=EXT[res_bin[:2]]
				with open("{0}/{1}{2}".format(DIR,key,ext),'wb') as f:
					f.write(res_bin)
			except KeyboardInterrupt:
				sys.exit()
			except:
				print(sys.exc_info()[1],"\n",item["MediaUrl"],"\n")		

	# jsonファイルから画像を取得
	# DIR is not decide
	def img_gets(self,json=DUMPFILE):
		EXT={b'\xff\xd8':'.jpg',b'\x47\x49':'.gif',b'\x89\x50':'.png'}
		mkdir("./{0}".format(self.search_word))
		# jsonから辞書を取得
		with open(DUMPFILE,'r') as f:
			results=load(f)

		for key,item in enumerate(results["d"]["results"]):
			try:
				res_bin=request.urlopen(item["MediaUrl"]).read()
				#res_bin=res_bin.read()
				# ヘッダを読んで拡張子を決定
				ext=EXT[res_bin[:2]]
				with open("./{0}/{1}{2}".format(self.search_word,key,ext),'wb') as f:
					f.write(res_bin)
			except:
				print(sys.exc_info()[1],"\n",item["MediaUrl"],"\n")		

if __name__=="__main__":
	app=Search()
	app.image("Tako",num=100)
	#app.img_gets('lp')
