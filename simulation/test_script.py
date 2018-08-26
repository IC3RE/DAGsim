# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 21:27:47 2018

@author: thoma
"""

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def setup(self):
        self.graph = []
        self.vote = []
    
    def result(self):
        
        for i in range(10):
            self.vote.append(i)
        print(self.vote)
    
Tom = Person('Tom', '22')
Tom.setup()
Tom.result()