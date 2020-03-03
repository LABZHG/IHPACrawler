# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 22:26:39 2020

@author: user
"""

import tensorflow as tf

class Layer:
    def __init__(self,shape,**kwargs):
        self.shape=shape
        self.judgeCF=False