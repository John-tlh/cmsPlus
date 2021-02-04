#!/usr/bin/env python3.8
# -*- encoding: utf-8 -*-
'''
@File    :   cmsPlus.py
@Contact :   kriller@cumt.edu.cn
@License :   (C)Copyright 2017-2021

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/2/2 22:31   kriller      1.0         None
'''

import HackRequests
from multiprocessing import process, Pool
import random
import time
import threading

fails = []

def Hackreq(host):
    path, names = getDict()
    urls = []
    threads = []
    for i in range(len(path)):
        urls.append(host+path[i])
        t = threading.Thread(target=worker,args=(host,urls[i],names[i]))
        threads.append(t)
        t.start()



def getDict():
    with open("data/dict.txt", "r") as file:
        lines = file.readlines()
        random.shuffle(lines)
        urls = []
        names = []
        for line in lines:
            names.append(line.split("------",2)[2])
            urls.append(line.split("------", 2)[0])
        return urls,names

def worker(host,url,name):
    hack = HackRequests.hackRequests()
    headers = {
        "Accept": "text / html, application / xhtml + xml, application / xml;",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0"
    }
    try:
        uu = hack.http(url, headers=headers,proxy=('127.0.0.1','7890'))
        if uu.status_code == 200:
            print(url + "  is activate !")
            print(host + "   maybe   " + name)
            return
        #只能打印成功识别到的
    except:
        pass
def getUrl():
    urls = []
    with open("url.txt", "r") as ufile:
        allurl = ufile.readlines()
        for i in range(len(allurl)):
            urls.append(allurl[i].strip('\n'))
        return urls

def getTitle():
    print("test")

if __name__ == '__main__':
    #使用多进程识别cms
    start_t = time.time()
    urls = getUrl()
    if(len(urls)>50):
        print("暂只支持一次性识别50个url！")
    print("需要识别的url数量为："+str(len(urls))+" 个")
    pool = Pool(len(urls))
    pool.map(Hackreq,urls)
    pool.close()
    pool.join()
    print("耗时："+str(time.time()-start_t))

