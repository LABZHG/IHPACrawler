# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 22:26:39 2020

@author: labzhg
"""

import tensorflow as tf

class Layer:
    def __init__(self,shape,vocab,embed,inputX,**kwargs):
        self.shape=shape
        self.judgeFC=False
        self.judgeSub=False
        self.applyBias=kwargs.get("apply_bias",True)
        self.vocabSize=vocab
        self.embed=embed
        self.inputX=inputX
        self.buildBlock()
        
    def buildBlock(self):
        with tf.name_scope("embedding"):
            self.embedding=tf.Variable(tf.random_uniform([self.vocabSize, \
                            self.embed], -1.0, 1.0),name="embedding")
            self.embeddingInputs = tf.nn.embedding_lookup(self.embedding,self.inputX)
            self.embeddingInputs = tf.expand_dims(self.embeddingInputs,-1)
        pooled=[]
        
    def inAnalysis():
        pass
