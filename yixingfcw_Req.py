# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 20:42:56 2020

@author: labzhg
"""

import requests
from bs4 import BeautifulSoup
#from openpyxl import Workbook
#from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
import re
import time
import xlsxwriter


def getURLpool(htmlcontent):
    tempIndex=htmlcontent.find("pagelist")
    endIndex=htmlcontent.find("尾页")
    content=htmlcontent[tempIndex:endIndex]
    SearchRe='href=\.*?(.*?)[>c]'
    SearchList=re.findall(SearchRe,content)
    global Pool
    Pool=URLpool()
    for A in SearchList[:-1]:
        Pool.Add("http://www.yxfcw.cn"+eval(A))
    for i in range(8,51):
        tempURL="http://www.yxfcw.cn/sale/"+"page"+str(i)+".html"
        if Pool.isInPool(tempURL):
            continue
        else:
            Pool.Add(tempURL)


def getData(htmlfile):
    wholeData=BeautifulSoup(htmlfile,"html.parser")
    Databegin=wholeData.div
    #father Tag
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
    #remove empty characters
    return DataList

'''
def DataOutput(bookList):
    Exbook=Workbook()
    Exsheet=Exbook.active
    Exsheet.title='sheet1'
    for i in range(0,len(bookList)):
        for j in range(0,len(bookList[i])):
            if ILLEGAL_CHARACTERS_RE.finditer(str(bookList[i][j])):
                ILLEGAL_CHARACTERS_RE.sub(r'', bookList[i][j].string)
            Exsheet.cell(row=i+1,column=j+1,value=str(bookList[i][j]))
    now = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time())) 
    path=now+r".xlsx"
    Exbook.save(path)
'''
    
def DataListOutput(OutList):
    now = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time())) 
    path=now+r".xlsx"
    outbook=xlsxwriter.Workbook(path)
    outsheet=outbook.add_worksheet('sheet1')
    for i in range(0,len(OutList)):
        for j in range(0,len(OutList[i])):
            outsheet.write(i,j,str(OutList[i][j]))
    outbook.close()
    
def coreDataBeneficiate(coreList):
    rowPtr=len(coreList)-1
    colStart=len(coreList[2])
    colEnd=len(coreList[rowPtr])
    #清洗头尾的多余无效字符
    for i in range(colStart,colEnd):
        del coreList[rowPtr][-1]
    del coreList[0:2]
    return coreList

def getURLcontent(url):
    try:
        clientType={'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'}
        wholeGet=requests.get(url,headers=clientType,timeout=70)
        #delay to avoid being blocked
        wholeGet.raise_for_status()
        wholeGet.encoding=wholeGet.apparent_encoding
        return wholeGet
    except:
        print("意外中止")

class URLpool: 
    #待访问URL的集合
    def __init__(self):
        self.visited=[]
        self.unvisited=[]
        
    def visArray(self):
        return self.visited
    
    def unvisArray(self):
        return self.unvisited
    
    def isVisited(self,URL):
        return URL in self.visited
    
    def isInPool(self,URL):
        return URL in self.unvisited
    
    def Visit(self,URL):
        return self.visited.append(URL)
    
    def Add(self,URL):
        return self.unvisited.append(URL)
    
    def clearPool(self):
        self.visited.clear()
        self.unvisited.clear()
        
    def isDone(self):
        return (len(self.unvisited) == 0)
    
    def getOne(self):
        try:
            return self.unvisited.pop()
        except:
            return None     

def ReqThread():
    #count=0
    while(not Pool.isDone()):
        newURL=Pool.getOne()
        newcontent=coreDataBeneficiate(getData(getURLcontent(newURL).text))
        for k in range(0,len(newcontent)):
            htmlData.append(newcontent[k])        
        ''''print('success')
        count=count+1
        print(count)'''

    

designative_url = "http://www.yxfcw.cn/sale/"
htmlText=getURLcontent(designative_url).text
getURLpool(htmlText)
Pool.Visit(designative_url)
htmlData=coreDataBeneficiate(getData(htmlText))
ReqThread()

DataListOutput(htmlData)

    


    