# -*- coding: utf-8 -*- 
import time
from ctypes import *
from io import BytesIO
import wave
import platform
import logging
import os

class XunFei(object):
    logging.basicConfig(level=logging.INFO)
    cur = cdll.LoadLibrary('/usr/lib/libmsc.so')
    #cur = cdll.LoadLibrary('./libmsc.so')

    def version(self,verName='ver_msc'):
        MSPGetVersion = self.cur.MSPGetVersion
        ret = 0
        v = MSPGetVersion(verName,ret)
        if ret != 0:
            logging.error("MSPLogin failed, error code: %s"  %(ret))
        else:
            logging.info("Version [%s]" %(v))
        return v    

    def login(self,str_txt='appid = 5947be90, work_dir = .'):
        MSPLogin = self.cur.MSPLogin
        ret = 0
        ret = MSPLogin(None,None,str_txt) 
        if ret != 0:
            logging.error("MSPLogin failed, error code: " + ret)
        else:
            logging.info("MSPLogin")
        return ret

    def search(self,src_text):
        MSPSearch = self.cur.MSPSearch
        MSPSearch.restype = c_char_p
        ret = 0
        text_finish = ''
        str_len = c_int(len(src_text))
        text_finish = MSPSearch("nlp_version =3.0,scene = main",src_text, byref(str_len),ret)
        if ret != 0:
            logging.error("MSPSearch failed, error code: %s"  %(ret))
        else:
            logging.info(str(text_finish))
        return text_finish

    def loginout(self):
        MSPLogout = self.cur.MSPLogout
        MSPLogout()
        logging.info("MSPLogout")

    def play(self,filename = 'test.wav'):
        import pygame
        pygame.mixer.init(frequency=16000)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

    def saveWave(self,raw_data,_tmpFile = 'test.wav'):
        f = wave.open(_tmpFile,'w')
        f.setparams((1, 2, 16000, 262720, 'NONE', 'not compressed'))
        f.writeframesraw(raw_data)
        f.close()
        return _tmpFile

    def text_to_speech(self,src_text="测试",file_name = None):
        
        QTTSSessionBegin = self.cur.QTTSSessionBegin
        QTTSTextPut = self.cur.QTTSTextPut

        QTTSAudioGet = self.cur.QTTSAudioGet
        QTTSAudioGet.restype = c_void_p

        QTTSSessionEnd = self.cur.QTTSSessionEnd
        ret = 0
        ret_c = c_int(0)
	#session_begin_params="engine_type = local,voice_name = xiaoyan, text_encoding = UTF8, tts_res_path = fo|res/tts/xiaoyan.jet;fo|res/tts/common.jet, sample_rate = 16000, speed = 50, volume = 50, pitch = 50, rdn = 2"
        session_begin_params="voice_name = vinn, text_encoding = utf8, sample_rate = 16000, speed = 50, volume = 50, pitch = 50, rdn = 2"
        sessionID = QTTSSessionBegin(session_begin_params, byref(ret_c))
        if ret_c.value != 0 :
            logging.error("QTTSSessionBegin failed, error code: %s" %(ret_c.value))
            return

        ret = QTTSTextPut(sessionID, src_text, len(src_text),None)
        if ret != 0:
            logging.error("QTTSTextPut failed, error code: %s"  %(ret))
            QTTSSessionEnd(sessionID, "TextPutError")
            
            return
        logging.info("正在合成 [%s]..." %(src_text))

        audio_len = c_uint(0)
        synth_status = c_int(0)

        f = BytesIO()
        while True:
            p = QTTSAudioGet(sessionID, byref(audio_len), byref(synth_status), byref(ret_c))
            if ret_c.value != 0:
                logging.error("QTTSAudioGet failed, error code: %s"  %(ret_c.value))
                QTTSSessionEnd(sessionID, "AudioGetError")
                break

            if p != None:
                buf = (c_char * audio_len.value).from_address(p)
                f.write(buf)

            if synth_status.value == 2 :
                self.saveWave(f.getvalue(),file_name)
                break

            logging.debug(".")
            time.sleep(1)

        logging.info('合成完成！')
        ret = QTTSSessionEnd(sessionID, "Normal")
        if ret != 0:
            logging.error("QTTSTextPut failed, error code: %s" %(ret))

    def speech_to_text(self,waveData):
        QISRSessionBegin = self.cur.QISRSessionBegin
        QISRAudioWrite = self.cur.QISRAudioWrite
        QISRGetResult = self.cur.QISRGetResult
        QISRGetResult.restype = c_void_p
        QISRSessionEnd = self.cur.QISRSessionEnd

        p_pcm = self.convDataToPointer(waveData)
        pcm_size = sizeof(p_pcm)
        
        ret_c = c_int(0)
        ret = 0
        ep_stat = c_int(0)
        rec_stat = c_int(0)


        logging.info("开始语音听写 ...")
        session_begin_params = "sub = iat, domain = iat, language = zh_cn, accent = mandarin, sample_rate = 16000, result_type = plain, result_encoding = utf8";
        sessionID = QISRSessionBegin(None,session_begin_params, byref(ret_c))
        if ret_c.value != 0 :
            logging.error("QISRSessionBegin failed, error code: %s" %(ret_c.value))
            return

        pcm_count = 0
        len = 10 * 640; #每次写入200ms音频(16k，16bit)：1帧音频20ms，10帧=200ms。16k采样率的16位音频，一帧的大小为640Byte
        while True:
            if pcm_size < 2 * len:
                len = pcm_size
            if len <= 0 :
                break

            aud_stat = 2
            if 0 == pcm_count:
                aud_stat = 1
                
            ret = QISRAudioWrite(sessionID, byref(p_pcm,pcm_count),len, aud_stat, byref(ep_stat), byref(rec_stat))
            if ret != 0:
                logging.error("QISRAudioWrite failed, error code: %s"  %(ret))
                break

            pcm_count += len
            pcm_size  -= len

            if ep_stat.value == 3:
                break
            time.sleep(.1)
    

        ret = QISRAudioWrite(sessionID, None,0, 4, byref(ep_stat), byref(rec_stat))
        if ret != 0:
            logging.error("QISRAudioWrite failed, error code: %s"  %(ret))

        error_c = c_int(0)
        text_finish = ""
        while  rec_stat.value != 5:
            x = QISRGetResult(sessionID, byref(rec_stat), 0, error_c)
            if x!=None:
                num = 0
                while True:
                    if (c_char).from_address(x+num).value != c_char('\x00').value:
                        num += 1
                    else:
                        break
                text = (c_char * num).from_address(x)
                text_finish += text.value

            time.sleep(.1)
        logging.debug(text_finish)
        logging.info('合成完成！')
        ret = QISRSessionEnd(sessionID, "Normal")
        if ret != 0:
            logging.error("QTTSTextPut failed, error code: %s"  %(ret))

        return text_finish

    def getWaveData(self,_tmpFile = 'test.wav'):
        with open(_tmpFile,'rb') as f:
            return f.read()

    def convDataToPointer(self,wav_data):
        tmpBytes = BytesIO()
        f_size = tmpBytes.write(wav_data)
        array = ( c_byte * f_size)()
        tmpBytes.seek(0,0)
        tmpBytes.readinto(array)
        return array


if __name__ == '__main__':
    xf = XunFei()
    xf.login()
    #xf.version() 
    #xf.search("合肥明天的天气怎么样?")
    xf.text_to_speech('讯飞SDK测试','xx.wav')
    #xf.play('xx.wav')
    #text = xf.speech_to_text(xf.getWaveData('xx.wav'))
    #print '识别结果:', text
    xf.loginout()
