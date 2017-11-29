#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import rospy
from voice_system.util import HelloGoodbye #Imports module. Not limited to modules in this pkg. 
from voice_system.xunfei import XunFei
from voice_system.tuling import Tuling
from voice_system.aiui import AIUI
from std_msgs.msg import String #Imports msg
import json

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Talker(object):
    def __init__(self):
        # Save the name of the node
        self.node_name = rospy.get_name()
        
        rospy.loginfo("[%s] 初始化." %(self.node_name))
        
        self.xf = XunFei()
        self.xf.login()
        self.xf.version()

        self.tl = Tuling()
        self.ai = AIUI()

        self.sub_topic_tts = rospy.Subscriber("~topic_tts",String, self.ttsTopic)
        self.pub_topic_tts = rospy.Publisher("~topic_tts",String, queue_size=1)

        self.pub_topic_input = rospy.Publisher("~topic_input",String, queue_size=1)
        # Setup subscriber
        self.sub_topic_input = rospy.Subscriber("~topic_input", String, self.inputTopic)
        # Read parameters
        self.pub_timestep = self.setupParameter("~pub_timestep",1.0)
        # Setup publishers
        self.pub_topic_a = rospy.Publisher("~topic_a",String, queue_size=1)
        # Create a timer that calls the cbTimer function every 1.0 second
        self.timer = rospy.Timer(rospy.Duration.from_sec(self.pub_timestep),self.cbTimer)

        rospy.loginfo("[%s] 初始化完成." %(self.node_name))

    def setupParameter(self,param_name,default_value):
        value = rospy.get_param(param_name,default_value)
        rospy.set_param(param_name,value) #Write to parameter server for transparancy
        rospy.loginfo("[%s] %s = %s " %(self.node_name,param_name,value))
        return value

    def ttsTopic(self,msg):
        #rospy.loginfo("[%s] %s" %(self.node_name,msg.data))
        rospy.loginfo("[%s] %s" %('回答',msg.data))
        self.xf.text_to_speech(msg.data)
        self.xf.play()

    def inputTopic(self,msg):
        #rospy.loginfo("[%s] %s" %(self.node_name,msg.data))
        rospy.loginfo("[%s] %s" %('问题',msg.data))
        data = self.xf.search(msg.data)
        rospy.logdebug("%s" %(data))
        if (self.ai.run(json.loads(data))== False):
            self.pub_topic_tts.publish(self.tl.search(msg.data))
        #self.pub_topic_tts.publish(self.tl.search(msg.data))
    def cbTimer(self,event):
        singer = HelloGoodbye()
        # Simulate hearing something
        msg = String()
        msg.data = singer.sing("duckietown")
        self.pub_topic_a.publish(msg)

    def on_shutdown(self):
        rospy.loginfo("[%s] Shutting down." %(self.node_name))


if __name__ == '__main__':
    # Initialize the node with rospy
    rospy.init_node('talker', anonymous=False)

    # Create the NodeName object
    node = Talker()

    # Setup proper shutdown behavior 
    rospy.on_shutdown(node.on_shutdown)
    
    # Keep it spinning to keep the node alive
    rospy.spin()
