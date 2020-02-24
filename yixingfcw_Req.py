# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 20:42:56 2020

@author: zhg
"""

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook


def getData(htmlfile):
    wholeData=BeautifulSoup(htmlfile,"html.parser")
    Databegin=wholeData.div
    for sibling in (Databegin.find_next_siblings()):
        if(sibling.attrs=={'id':'yimao1200'}):
            getList=sibling
    finalList=[]
    tempRow=[]
    for dTag in getList.findAll('li'):
        if(dTag.string):
            tempRow.append(dTag.string)
        else:
            if(len(tempRow)):
                finalList.append(tempRow[:])
            tempRow.clear()
            continue  
    DataList = list(filter(None, finalList)) 
    return DataList

def demoOutput(demoList):
    Exbook=Workbook()
    Exsheet=Exbook.active
    Exsheet.title='sheet1'
    for i in range(0,len(demoList)):
        for j in range(0,len(demoList[i])):
            Exsheet.cell(row=i+1,column=j+1,value=str(demoList[i][j]))
    Exbook.save('demo.xlsx')
    
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
demoOutput(htmlData)

    


    