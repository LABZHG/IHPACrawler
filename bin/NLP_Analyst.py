# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 22:26:39 2020

@author: labzhg
"""

import tensorflow as tf
import numpy as np
import os
from loss.loss import cross_entropy_loss
from eval.evaluate import accuracy
from tensorflow.contrib import slim
from snownlp import SnowNLP

class Layer:
    def __init__(self,numClasses,seqLen,vocab,embeddingDim,learningRate,
                 learningDecayRate,learningDecaySteps,epoch,dropout):
        self.numClasses = numClasses
        self.seqLen = seqLen
        self.vocab = vocab
        self.embeddingDim = embeddingDim
        self.learningRate = learningRate
        self.learningDecayRate = learningDecayRate
        self.learningDecaySteps = learningDecaySteps
        self.epoch = epoch
        self.dropout = dropout
        self.inputX = tf.placeholder(tf.int32, [None, self.seqLen], name='inputX')
        self.inputY = tf.placeholder(tf.float32, [None, self.numClasses], name='inputY')
        self.buildBlock()
        
    def buildBlock(self):
        with tf.name_scope("embedding"):
            self.embedding=tf.Variable(tf.random_uniform([self.vocabSize, \
                            self.embed], -1.0, 1.0),name="embedding")
            self.embeddingInputs = tf.nn.embedding_lookup(self.embedding,self.inputX)
            self.embeddingInputs = tf.expand_dims(self.embeddingInputs,-1)
        
        with tf.name_scope("embedding"):
            self.embedding = tf.get_variable("embedding", [self.vocab, self.embeddingDim])
            embedding_inputs = tf.nn.embedding_lookup(self.embedding, self.inputX)
 
        with tf.name_scope("dropout"):
            dropout_output = tf.nn.dropout(embedding_inputs, self.dropout)

        with tf.name_scope("average"):
            mean_sentence = tf.reduce_mean(dropout_output, axis=1)
 
        with tf.name_scope("score"):
            self.logits = tf.layers.dense(mean_sentence, self.numClasses,name='dense_layer')
 
        self.loss = cross_entropy_loss(logits=self.logits,labels=self.inputY)
 
        self.global_step = tf.train.get_or_create_global_step()
        learningRate = tf.train.exponential_decay(self.learningRate, self.global_step,
                                                   self.learningDecaySteps, self.learningDecayRate,
                                                   staircase=True)
 
        optimizer= tf.train.AdamOptimizer(learningRate)
        update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
        self.optim = slim.learning.create_train_op(total_loss=self.loss, optimizer=optimizer,update_ops=update_ops)
        self.acc = accuracy(logits=self.logits,labels=self.inputY)
 
    def fit(self,train_x,train_y,val_x,val_y,batch_size):
        if not os.path.exists('./saves/fasttext'): os.makedirs('./saves/fasttext')
        if not os.path.exists('./train_logs/fasttext'): os.makedirs('./train_logs/fasttext')

        trainStep = 0
        bestacc = 0
        tf.summary.scalar('lossVal', self.loss)
        tf.summary.scalar('accVal', self.acc)
        merged = tf.summary.merge_all()
 
        sess = tf.Session()
        writer = tf.summary.FileWriter('./train_logs/fasttext', sess.graph)
        saver = tf.train.Saver(max_to_keep=10)
        sess.run(tf.global_variables_initializer())
 
        for i in range(self.epoch):
            trainBatch = self.batch_iter(train_x, train_y, batch_size)
            for batch_x,batch_y in trainBatch:
                trainStep += 1
                feed_dict = {self.inputX:batch_x,self.inputY:batch_y}
                _, trainloss, trainacc = sess.run([self.optim,self.loss,self.acc],feed_dict=feed_dict)
 
                if trainStep % 1000 == 0:
                    feed_dict = {self.inputX:val_x,self.inputY:val_y}
                    lossVal,accVal = sess.run([self.loss,self.acc],feed_dict=feed_dict)
 
                    summary = sess.run(merged,feed_dict=feed_dict)
                    writer.add_summary(summary, global_step=trainStep)
 
                    if accVal>=bestacc:
                        bestacc = accVal
                        saver.save(sess, "./saves/fasttext/", global_step=trainStep)
 
                    msg = 'epoch:%d/%d,trainStep:%d,trainloss:%.4f,trainacc:%.4f,lossVal:%.4f,accVal:%.4f'
                    print(msg % (i,self.epoch,trainStep,trainloss,trainacc,lossVal,accVal))
 
    def batch_iter(self, x, y, batch_size=32, shuffle=True):
        data_len = len(x)
        num_batch = int((data_len - 1) / batch_size) + 1
 
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_len))
            shuffleX = x[shuffle_indices]
            shuffleY = y[shuffle_indices]
        else:
            shuffleX = x
            shuffleY = y
        for i in range(num_batch):
            start_index = i * batch_size
            end_index = min((i + 1) * batch_size, data_len)
            yield (shuffleX[start_index:end_index], shuffleY[start_index:end_index])
 
    def predict(self,x):
        sess = tf.Session()
 
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver(tf.global_variables())
        ckpt = tf.train.get_checkpoint_state('./saves/fasttext/')
        saver.restore(sess, ckpt.model_checkpoint_path)
 
        feed_dict = {self.inputX: x}
        logits = sess.run(self.logits, feed_dict=feed_dict)
        y_pred = np.argmax(logits, 1)
        return y_pred

def getKeywordsToJudge(text):
    context = SnowNLP(text)
    num = 5
    JudgeList={}
    for single in context.sentences:
        keywords = single.keywords(num)
        for word in keywords:
            JudgeList.update({word:single})
    return keywords