# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 13:37:42 2021

@author: Acer User
"""


import sys
from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error 
import xlwt
import sqlite3



#coding = utf-8
def main():
    baseurl = "https://movie.douban.com/top250?start="
    #parse the website to get data
    datalist = getdata(baseurl)
    #Save Data
    savepath = "D:/Users/Acer User/Desktop/Douban Top250.xls"
    savedata(datalist,savepath) 
    askURL("https://movie.douban.com/top250?start=")

#Define the pattern of data you want to search
#Get the movie link
findLink = re.compile(r'<a href="(.*?)">')
#Get the movie image
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S) 
#re.S is to let the new line symbol included
#Movie Name
findTitle = re.compile(r'<span class="title">(.*)</span>')
#Movie Rating
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#Number of People rate the movie
findJudge = re.compile(r'<span>(\d*)人评价</span>') #\d = number *= 0-more number
#Movie Overview
findInq = re.compile(r'<span class="inq">(.*)</span>')
#Movie related information (Director, Actors, Actresses,Movie Type)
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)



#Website parsing   
def getdata(baseurl):
    datalist = []
    for i in range(0,10):#There are total 10 pages in top250 douban movie
        url = baseurl+str(i*25) #In each page, there are 25 items 
        html = askURL(url)
    #Parse the data one by one
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all("div",class_="item"):
            #Find eligible string, then turn into list
            #print(item) 
            data = [] #Save all the information of a movie
            item = str(item)
            
            #Movie Link
            link = re.findall(findLink, item)[0]
            data.append(link)
            
            #Movie Image
            ImgSrc = re.findall(findImgSrc,item)[0]
            data.append(ImgSrc)
            
            #Movie Titles
            titles = re.findall(findTitle,item) #Only need chinese and english title
            if len(titles) == 2:
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("/","")  #use replace to remove /
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(" ")
            
            #Movie Rating
            rating = re.findall(findRating,item)[0]
            data.append(rating)
            
            #Number of Judge
            judgeNum = re.findall(findJudge,item)[0]
            data.append(judgeNum)
            
            #Movie Overview
            inq = re.findall(findInq,item)
            if len(inq) != 0:
                inq = inq[0].replace("。"," ") 
                data.append(inq)
            else:
                data.append(" ")
                
            #Movie related information
            bd = re.findall(findBd,item)[0]
            bd = re.sub("<br(\s+)?/>(\s)?"," ",bd)
            bd = re.sub("/"," ",bd)
            data.append(bd.strip()) #Remove black space
            
            datalist.append(data)
            
        
    print(datalist)    
    return datalist

#Get specific URL information
def askURL(url):
    #Tell the url you visit, which type of agent you are
    head={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30"}
    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
            
    return html
            




#Save Data
def savedata(datalist,savepath):
    print("Data saved")
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet('Douban Movie Top250',cell_overwrite_ok = True)
    col = ("Movie Link","Movie Photo","Movie Chinese Name","Movie English Name",
           "Rating","No. of Judge","Overview","Movie Related Information")
    for i in range(0, 8):
        sheet.write(0,i,col[i])
    for i in range(0,250):
        print("%d item"%i)
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j]) #Start from row 2, because row 1 is column name
    book.save(savepath)
    
if __name__ == "__main__":
    main()
    print("Done")