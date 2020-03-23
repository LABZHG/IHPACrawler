# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 22:42:43 2020

@author: labzhg
"""

from pymongo import MongoClient
from bson import ObjectId
import xlrd
import json

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

def FindData(datakey,dataval,Id='',multi=False):
    if(multi):
        return DBase[dbTable].find({datakey:dataval})
    else:
        if(Id):
            ret=DBase[dbTable].find_one({'_id':ObjectId(Id)})
        else:
            ret=DBase[dbTable].find_one({datakey:dataval})
        return ret

def countNums():
    return DBase[dbTable].count_documents({})

def readExcel(filePath):
    preData=xlrd._workbook(filePath)
    tableData=preData.sheets()[0]
    readData={}
    rows=tableData.nrows
    tags=DBase[dbTable].find_one()
    for i in range(rows):
        readData[i]=json.dumps(dict(zip(tags,tableData.row_values(i))))
        readData[i]=json.loads(readData[i])
        insertSingleData(readData[i])


    
