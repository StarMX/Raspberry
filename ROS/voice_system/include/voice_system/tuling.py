# -*- coding: utf-8 -*- 
import requests

class Tuling(object):
    key = "62142b9812c745509cc5e1dd6010c898"
    #key = "3a4b739e59bf4ec4a7b0a5baee492889"
    apiurl = "http://www.tuling123.com/openapi/api"
    #apiurl = "http://openapi.tuling123.com/openapi/api"

  
    def search(self, info):
        re = requests.post(self.apiurl, data={'key':self.key,'info':info,'userid':'123456','loc':'武汉市烽火村'})
        re_dict = re.json()
        return re_dict['text']
