# -*- coding: utf-8 -*-
import pyaudio
import wave
from array import array
import rospy

class microphone:

    def __init__(self,savepath):
        self.savepath=savepath
        self.sleepflag=0
    def getSleepFLag(self):
        return self.sleepflag
    def getRate(self):
        return 16000

    def silent(self,recorddata):
        return max(array('h', recorddata))<self.slientThreshold()

    def slientThreshold(self):
        return 5000

    def recordAudio(self):
        NUM_SILENT=20
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1 # 0,1
        RECORD_SECONDS=3
        RATE = self.getRate() #采样频率
        WAVE_OUTPUT_FILENAME = self.savepath
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
        rospy.logdebug("* recording")
        frames = []
        num_silent=0
        longtime=int(RATE / CHUNK * RECORD_SECONDS) # if time is belong 5 ,force stop
        counter=0
        while 1:
            counter +=1
            data = stream.read(CHUNK)
            frames.append(data)
            silent=self.silent(data)
            if silent:
                num_silent += 1
                rospy.logdebug("* sleeping")
            else:
                self.sleepflag +=1
                num_silent = 0
                rospy.logdebug("* active")
            if num_silent>=NUM_SILENT:
                rospy.logdebug("* sleeping too long")
                break
            if counter>longtime:
                rospy.logdebug("* record time out")
                break
        rospy.logdebug("* done recording")
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()