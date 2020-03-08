# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 22:42:43 2020

@author: labzhg
"""

from pymongo import MongoClient

Mongo_URL="mongodb://localhost:2100"
dbName="FullMessage"
dbTable="__date__"

client=MongoClient(Mongo_URL)
DBase=client[dbName]

def insertSingleData(data):
    if (DBase[dbTable].insert_one(data)):
        return True
    else:
        return False;

def insertManyData(datalist:list):
    if (DBase[dbTable].insert_many(datalist)):
        return True
    else:
        return False;

def FindData(datakey,dataval):
    ret=DBase[dbTable].find_one({datakey:dataval})
    return ret
    
