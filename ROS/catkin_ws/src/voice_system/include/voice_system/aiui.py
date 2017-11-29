# -*- coding: utf-8 -*- 
#import json
import rospy
from std_msgs.msg import String
import tuling
import subprocess
import json


class AIUI(object):
    p = None
    def __init__(self):
        self.pub_topic_tts = rospy.Publisher("~topic_tts",String, queue_size=1)
        self.service = {
            'weather': self.__default,
            'chat': self.__default,
            'poetry': self.__default,
            #'story':self.__story, #未开放
            'musicX': self.__music, #未开放
            'weather': self.__default,
            'cookbook': self.__cookbook,
            'news': self.__news,
            'cmd': self.__cmd,
            'joke':self.__joke
        }
    
    def __music(self):
        import requests
        #rospy.logerr(json.dumps(self.json).decode('utf-8'))
        #music = {}
        music = []
        song = self.json['semantic'][0]['slots']  
        for index in range(len(song)):
            #music[song[index]["name"]]=song[index]["value"]
            music.append(song[index]["value"])
        rospy.logerr(' '.join(music))    
        re = requests.get('http://tingapi.ting.baidu.com/v1/restserver/ting?format=json&from=webapp_music&method=baidu.ting.search.catalogSug&query='+ ' '.join(music))
        re_dict = json.loads(re.text)
        songid = re_dict['song'][0]['songid']
        re = requests.get('http://tingapi.ting.baidu.com/v1/restserver/ting?format=json&from=webapp_music&method=baidu.ting.song.play&songid='+ songid)
        re_dict = json.loads(re.text)

        self.play(re_dict['bitrate']['show_link'])

        # rospy.logerr(json.dumps(re_dict, ensure_ascii=False))
        #self.pub_topic_tts.publish(json.dumps(music, ensure_ascii=False))

    def __joke(self):
        self.play(self.json['data']['result'][0]['mp3Url'])
        #rospy.logerr('err %s %s',self.json['text'] ,self.json['data']['result'][0]['mp3Url'])

    def __cmd(self):
        rospy.logerr('err %s %s',self.json['text'] ,self.json['semantic'])

    def __cookbook(self):
        self.__default() 
        self.pub_topic_tts.publish(self.json['data']['result'][0]['steps'])

    def __story(self):
        self.play(self.json['data']['result'][0]['playUrl'])
        #self.__default()  

    def __news(self):
        self.play(self.json['data']['result'][0]['url'])

    def __error(self):
        if ('answer' in self.json.keys()):
            self.__default()
        rospy.logerr('err %s %s %s',self.json['service'] ,self.json['text'] ,json.dumps(self.json).decode('utf-8'))

    def __default(self):
        self.pub_topic_tts.publish(self.json['answer']['text'])

    def run(self,jsonData):
        self.json = jsonData
        if (self.json['rc']==0):
            print 'AIUI > %s' %(self.json['service'])
            if ('_smartHome' in self.json['service']):
                rospy.logerr('err %s %s',self.json['service'] ,json.dumps(self.json, ensure_ascii=False))
                self.pub_topic_tts.publish('技能缺失')
            else:
                func = self.service.get(self.json['service'],self.__error)
                func()
            return True
        elif (json['rc']==4):
            rospy.logerr('AIUI err rc %s',self.json['rc'])
            return False


    def play(self,filename):
        self.stop()
        self.p = subprocess.Popen(["mpg123", filename]) #mpg123

    def stop(self):
        if self.p:
            self.p.terminate()
            self.p = None            