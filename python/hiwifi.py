#!/usr/bin/python
#coding=utf-8

import os
import json
import requests
import ctypes,subprocess
import logging

logging.basicConfig(level=None)

class Chat(object):
    apiurl = "http://app.hiwifi.com/plugin"

    def init(self):
        #os.system("clear")
        print 'run'


  
    def get(self, info='1631165351'):
		s = requests.Session()
		response = s.get(self.apiurl + '?sid=' + str(info),verify=False, cookies={'__uuid':'ezuUQ1lH4kYDhIBgMLkEAg==','ppinfo':'1499588209%7CdWlkOjc6MTM2MzUxNHx1c2VybmFtZTo1OlN0YXJafA%3D%3D%7C', 'ppuid':'u62803018450','ppuserinfo':'1499588209%7CcNgIf8HucEuezjKJ58vCbilDzvllzqIkHZPRMD5e6w%7C1467217436'})
		#response.encoding = response.apparent_encoding
        #re = requests.get(self.apiurl, data={'m':'plugins','a':'install','rid':'r65905684198','sid':info}, cookies=dict(__uuid='ezuUQ1lH4kYDhIBgMLkEAg==', ppuid='u62803018450'))
		al = response.content
		#print response.text.decode('utf-8')
		title = al[al.find('<title>') + 7 : al.find('</title>')].decode('utf-8')
		if (title!='提示信息 - 极路由云平台'.decode('utf-8')):
			print title

			file_object = open('thefile.txt', 'a')
			file_object.write((title + str(info) +'\n').encode('utf-8') )
			file_object.close()
		#html_doc=str(html,'utf-8') #html_doc=html.decode("utf-8","ignore")
		#print(html_doc)
        #re_dict = re.json()
		#re.encoding = 'gb2312'
        #text = re.text.encode(re.encoding).decode('utf-8') # re_dict['text']
        #print text 


if __name__ == "__main__":
	chat = Chat()
	chat.init()
	for i in range(1,10000):
		chat.get(i)