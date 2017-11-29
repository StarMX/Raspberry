#!/usr/bin/python
#coding=utf-8

import os
import json
import requests
import ctypes,subprocess
import xunfei
import json

class Chat(object):
    key = "62142b9812c745509cc5e1dd6010c898"    # turing123网站
    apiurl = "http://www.tuling123.com/openapi/api"
    xf = xunfei.XunFei()

    def init(self):
        os.system("clear")
        self.xf.login()
        print "尽情调教把!"
        print "-------------------------------"
        
    def luyin():
        os.system('arecord  -D plughw:1,0 -c 1 -d 2  xx.wav -r 8000 -f S16_LE 2>/dev/null')

    def get(self):
        print "> ",
        info = raw_input()
        if (info == 'q' or info == 'exit' or info == "quit"):
            print "- Goodbye"
            return
        self.send(info)
  
    def send(self, info):
        re = requests.post(self.apiurl, data={'key':self.key,'info':info})
        re_dict = re.json()
        text = re_dict['text'].encode('utf-8')
	#text = '啊哦~~这个问题太难了，换个问题吧！'
	#test = self.xf.search(info)
	#print test
	#re_dict = json.loads(test)
	#if (re_dict['rc'] == 0):
        #    text = re_dict['answer']['text'].encode('utf-8')
        print '- ', text
        self.xf.text_to_speech(text,'xx.wav')
        self.xf.play('xx.wav')
        self.get()


if __name__ == "__main__":
    chat = Chat()
    chat.init()
    chat.get()
