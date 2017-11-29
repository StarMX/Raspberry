# -*- coding: utf-8 -*- 
import random

# Implement modules
class HelloGoodbye(object):
    def __init__(self):
        self.word_list = ['你好','再见']
    
    def sing(self,name):
        return random.choice(self.word_list) + ", " + name + "."

if __name__ == '__main__':
    # Test code for ModuleName
    module = HelloGoodbye()
    print module.sing('duckietown')

