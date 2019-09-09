'''此脚本主要是用来批量探测ip和域名是否可以被访问换句话说是否部署了web服务'''
#-*- coding:utf-8 -*-
# Python 3.5
# Author: 白猫 <cyber-security@qq.com>
import requests,re
#读取文件每一行并将文件内容存放在列表中
def content2List(add):
    # cwd=os.getcwd()
    dirList=[]
    # add=cwd+"\\dict\\directory.txt"
    f=open(add,"rb")
    for line in f.readlines():
        line=str(line,encoding="utf-8")
        line = line.replace("\n","")
        line = line.replace("\t","")
        line = line.replace("\r","")
        line = line.replace("\s","")
        # dirList.append(str(line)[2:-5])
        dirList.append(line)
    return dirList
#将字符串设定为统一长度
def setStr2SameLen(length,string):
    if length>len(string):
        length=length-len(string)
        for i in range(length):
            string=string+' '
        return string
    else:
        return string
def detective():
    add="E:\\渗透测试\\2019\\2019-1\\浙江移动\\url_new.txt"
    info = content2List(add)
    for i in info:
        url="http://"+i
        try:
            res = requests.get(url,timeout=3)
            msg1=setStr2SameLen(40,i)+'可访问'
            print('[+]'+msg1)
        except:
            msg2=setStr2SameLen(40,i)+'不可访问'
            print('[-]'+msg2)

if __name__=='__main__':
    detective()