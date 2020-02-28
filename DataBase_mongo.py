# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 22:42:43 2020

@author: labzhg
"""

from pymongo import MongoClient

Mongo_URL="mongodb://localhost:2100"

client=MongoClient(Mongo_URL)