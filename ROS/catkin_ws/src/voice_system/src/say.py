#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import rospy
from std_msgs.msg import String

class MyChat(object):
    def __init__(self):
        rospy.loginfo("开始发消息吧")
        self.pub=rospy.Publisher('/talker/topic_input',String,queue_size=10)
    #     self.say()
    #     pub_period = rospy.get_param("~pub_period",1.0)
    #     rospy.Timer(rospy.Duration.from_sec(pub_period),self.callback)

    # def callback(self,event):
    #     msg = String()
    #     msg.data = "%s is %s!" %('11111','222222222')
    #     self.pub.publish(msg)

    def say(self):
        info = raw_input(">")
        if (info == 'q' or info == 'exit'):
            exit()
            return
        rospy.loginfo(info)
        msg = String()
        msg.data = info
        self.pub.publish(msg)
        self.say()

if __name__ == '__main__':
    rospy.init_node('input', anonymous=False)
    c = MyChat()
    c.say()
    rospy.spin()    