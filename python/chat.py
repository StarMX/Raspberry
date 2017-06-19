#!/usr/bin/python
#coding=utf-8

import os
import json
import requests
import ctypes,subprocess
import xunfei

class Chat(object):
    key = "62142b9812c745509cc5e1dd6010c898"    # turing123网站
    apiurl = "http://www.tuling123.com/openapi/api"
    xf = xunfei.XunFei()

    def init(self):
        os.system("clear")
        self.xf.login()
        print "尽情调教把!"
        print "-------------------------------"
  
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
        text = re_dict['text']
        print '- ', text
        self.xf.text_to_speech(text.encode('utf-8'),'xx.wav')
        self.xf.play('xx.wav')
        self.get()


if __name__ == "__main__":
    chat = Chat()
    chat.init()
    chat.get()
    #xf.loginout()