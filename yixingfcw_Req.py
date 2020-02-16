# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 20:42:56 2020

@author: zhg
"""

import requests
from bs4 import BeautifulSoup

def getData(htmlfile):
    wholeData=BeautifulSoup(htmlfile,"html.parser")
    Datademo=wholeData.a.string
    for sibling in (wholeData.li.parents):
        print(sibling)
    return Datademo

def coreDataBeneficiate():
    pass

def getURLcontent(url):
    try:
        clientType={'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'}
        wholeGet=requests.get(url,headers=clientType,timeout=20)
        wholeGet.raise_for_status()
        wholeGet.encoding=wholeGet.apparent_encoding
        return wholeGet
    except:
        print("意外中止")
        

designative_url = "http://www.yxfcw.cn/sale/"
htmlText=getURLcontent(designative_url).text
htmlData=getData(htmlText)
#print(htmlData)

    


    