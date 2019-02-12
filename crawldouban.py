# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 21:44:58 2019

@author: 99364
"""

import requests
import sys
import importlib
import re
from bs4 import BeautifulSoup
import traceback
import random
import time
import xlwt

# 定义所需函数
def getHTMLText(req,url):
    try:
        tl = random.uniform(2,5)
        time.sleep(tl)
        req = req
        r = req.get(url)
        #print(r.status_code)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('getHTMLText出错')

def getShortCommentInformation1(req,lst,commentURL):
    html = getHTMLText(req,commentURL)
    #print(html)
    soup = BeautifulSoup(html,'html.parser')
    div = soup.find_all('div',class_='comment-item')
    #print(div)
    for i in div:
        try:
            #print(i)
            # 一级网页信息
            a = i.find_all('span',class_='votes')
            Votes = a[0].string
            #print(Votes)
            href = i.find_all('a')
            #print(href[0].attrs['href'])
            perstar = i.h3.find_all('span',class_='comment-info')
            #print(perstar)
            perstar1 = perstar[0].contents[5].attrs['class'][0]
            #print(perstar1)
            star = re.search(r'\d',perstar1).group(0)
            #print(star)
            p = i.find_all('span',class_='short')
            #print(p[0].span.string)
            
            # 二级网页信息
            html1 = getHTMLText(req,href[0].attrs['href'])
            #print(html1)
            soup1 = BeautifulSoup(html1,'html.parser')
            t =soup1.find_all('div',class_='user-info')
            t1 = re.search(r'20[0,1]\d',t[0].text).group(0)
            time = 2019 - int(t1)
            #print(time)
            link0 = 'https://www.'+re.search(r'douban.+',href[0].attrs['href']).group(0)+'rev_contacts'
            #print(link0)
            f = soup1.find_all('a',href=link0)
            #print(f)
            fans = re.search(r'\d+',f[0].text).group(0)
            #print(fans)
            link = 'https://movie.'+re.search(r'douban.+',href[0].attrs['href']).group(0)+'collect'
            #print(link)
            m = soup1.find_all('a',href=link)
            #print(m)
            movies = re.search(r'\d+',m[0].text).group(0)
            #print(movies)
            
            # 二级数组，存储每个人的信息
            z = [Votes,star,p[0].string,time,fans,movies]
            
            # 一级数组，存储爬取到的所有信息
            lst.append(z)
        except:
            continue
        
def main():
    # 模拟登陆
    req = requests.Session()

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    url = 'https://accounts.douban.com/j/mobile/login/basic'
    data = {
            'ck': '',
            'name':'15958846537',
            'password':'zhengshujin54101',
            'remenber':'false',
            'ticket':''
            }
    r = req.post(url, data, headers=headers,timeout=8)
    
    # 爬取网页内容
    slist = []
    ye = int(input('需要爬取的页数:'))+1
    for i in range(1,ye):
        x = random.uniform(0,1)
        time.sleep(x)
        commentURL = 'https://movie.douban.com/subject/26266893/comments?start='+str((int(i)-1)*20)+'&limit=20&sort=new_score&status=P'
        #print(commentURL)
        getShortCommentInformation1(req,slist,commentURL)
    
    # 写入Excel    
    we = xlwt.Workbook()    
    sheet1 = we.add_sheet(u'豆瓣流浪地球短评',cell_overwrite_ok=True)
    rowTitle = [u'编号',u'短评被点赞数',u'星级',u'短评',u'评论人用豆瓣时间','粉丝数',u'评论人看过电影的数量']
    rowDatas = slist
    
    for i in range(0,len(rowTitle)):
        sheet1.write(0,i,rowTitle[i])
    
    for k in range(0,len(rowDatas)):    #先遍历外层的集合，即每行数据
        rowDatas[k].insert(0,k+1)   #每一行数据插上编号即为每一个人插上编号
        for j in range(0,len(rowDatas[k])): #再遍历内层集合
            sheet1.write(k+1,j,rowDatas[k][j]) #写入数据,k+1表示先去掉标题行，另外每一行数据也会变化,j正好表示第一列数据的变化，rowdatas[k][j] 插入数据
    we.save('C:/Users/99364/Desktop/python/wandering_earth.xlsx')
    
if __name__ == '__main__':
    main()
    
    
    
    