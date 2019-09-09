# -*- coding: utf-8 -*-
'''
    author      : ba1ma0
    platform    : Windows & Python3
    description : 该文件实现的主要功能是利用awvs的APIkey批量创建扫描任务
    How2Use     : 用户只需修改AWVS配置区的相关信息即可,然后保存运行 python awvs.py
'''
import json,time,requests,urllib3,psycopg2,datetime
from module import tool
urllib3.disable_warnings()
requests.adapters.DEFAULT_RETRIES = 5
#获取当前的时间比如12:20:13
current_time = time.strftime("%X",time.localtime())
#taskInfo主要用来存储taskId和taskName   
taskInfo = {}
########################  AWVS 相关配置信息区   ##################################
apikey_awvs = "1986ad8c0a5b3df4d7028d5f3c06e936ca687f4b200384755b15e531c1aeb4503"       #awvsAPIkey值, Administrator>profile>API Key>generate API
host        = "49.234.98.25"                                                            #主机地址
port        = "45432"                                                                   #awvs默认端口号
database    = "wvs"                                                                     #awvs数据库默认名称
user        = "acunetix"                                                                #awvs的默认用户名
password    = "UxeOMHYzbPAqpRSGabPdnQQ2d6wSTRKS"                                        #连接awvs的密码
########################  AWVS 相关配置信息区   ##################################
#add         = "D:\\Github\\butian\\test.txt"                                            #待扫描站点txt文件地址
#start_date  = "20190724T122000+0800"                                                    #开始扫描的时间,0800是东8时区区
#speed       = "s"                                                                       #扫描速度,有f(快速扫描),m(中速扫描),s(慢扫描)三个选项
#scan_profile= "F"                                                                       #扫描类型,有H(高危漏洞扫描),W(弱口令扫描),C(爬虫),X(跨站脚本攻击),S(SQL注入扫描),F(全扫描)
host_awvs   = "https://"+str(host)+":13443/"                                             #awvs所在主机地址
#awvs添加任务时添加任务时请求的URL
url_awvs =  str(host_awvs)+"/api/v1/targets"
#awvs请求头构造,awvs的api验证依靠请求头
header_awvs = {"X-Auth":apikey_awvs,"content-type":"application/json"}
#扫描级别,1:只扫高危,2:弱口令检测,3:爬虫,4:跨站脚本,5:SQL注入,6:全扫描
profile = {
"H":'11111111-1111-1111-1111-111111111112',    #High Risk Vulnerabilities
"W":'11111111-1111-1111-1111-111111111115',    #Weak Passwords
"C":'11111111-1111-1111-1111-111111111117',    #Crawl Only
"X":'11111111-1111-1111-1111-111111111116',    #Cross-site Scripting Vulnerabilities
"S":'11111111-1111-1111-1111-111111111113',    #SQL Injection Vulnerabilities
"F":'11111111-1111-1111-1111-111111111111'     #Full Scan
}
profile_show = {
"H":'High Vulnerabilities',                   #High Risk Vulnerabilities
"W":'  Weak Passwords',                       #Weak Passwords
"C":'  Crawl Only',                           #Crawl Only
"X":'XSS Vulnerabilities',                    #Cross-site Scripting Vulnerabilities
"S":'  SQL Injection ',                       #SQL Injection Vulnerabilities
"F":'     Full Scan'                             #Full Scan
}
#扫描速度
scan_speed = {
    "s":"  slow",
    "m":"  moderate",
    "f":"  fast",
}
#将awvs的时间改为标准时间20190724T122000+0800 -> 2019-07-24 12:20:00并返回字典的形式{"y":"2019","m":"07","d":"12","h":"12","m":"20","s":"00"}
def awvs2standardTime(awvs_time):
    standard_time = awvs_time.replace("+0800","")
    standard_time = standard_time.replace("T","")
    year             = standard_time[0:4]             
    month            = standard_time[4:6]
    day              = standard_time[6:8]
    hour             = standard_time[8:10]
    minute           = standard_time[10:12]
    second           = standard_time[12:14]
    return {
        "year"   :  year,
        "month"  :  month,
        "day"    :  day,
        "hour"   :  hour,
        "minute" :  minute,
        "second" :  second
    }

#将标准时间转化为awvs时间2019-07-24 12:20:00 ->20190724T122000+0800 
def time2awvstime(standard_time):
    standard_time = standard_time.replace("-","")
    standard_time = standard_time.replace(":","")
    standard_time = standard_time.replace(" ","")
    awvs_time     = str(standard_time[0:8])+str("T")+str(standard_time[8:14])+str("+0800")
    return awvs_time

#该函数主要是改变时间n秒之后时间,present_time参数是标准的字典格式{"y":"2019","m":"07","d":"12","h":"12","m":"20","s":"00"},但返回结果是标准的2019-07-27 12:20:00
def nSecondLatter(present_time,second):
    import re
    
    nSecond                         =    int(present_time["second"]) +  second
    present_time["second"]          =    nSecond % 60                                      #n秒之后秒针应该对应的时间
    if len(str(present_time["second"]))  == 1:
        present_time["second"]      = str(0) + str(present_time["second"])
    
    nMinute                         =    int(present_time["minute"]) + nSecond // 60   
    present_time["minute"]          =    nMinute % 60                                      #n秒之后分针应该对应的时间
    if len(str(present_time["minute"]))  == 1:
        present_time["minute"]      = str(0) + str(present_time["minute"])
    
    nHour                           =    int(present_time["hour"])   + nMinute // 60       
    present_time["hour"]            =    nHour   % 24                                      #n秒之后时针应该对应的时间
    if len(str(present_time["hour"]))    == 1:
        present_time["hour"]        = str(0) + str(present_time["hour"])
    
    future_time                     =    str(present_time["year"])+"-"+str(present_time["month"])+"-"+str(present_time["day"])+" "+str(present_time["hour"])+":"+str(present_time["minute"])+":"+str(present_time["second"])
    if nHour   // 24 !=0:
        now_time    = datetime.datetime(int (present_time["year"]),int (present_time["month"]),int (present_time["day"]),int (present_time["hour"]),int (present_time["minute"]),int (present_time["second"]),int (000000))
        future_time = str(now_time + datetime.timedelta(days=(nHour//24)))
    return future_time

#awvs中添加扫描任务
def add_tasks(address,description,criticality,speed):
    global taskInfo,scan_speed,url_awvs
    try:
        current_time = time.strftime("%X",time.localtime())
        speed = scan_speed[speed]
        data = {"address":address,"description":description,"criticality":criticality}
        data = json.dumps(data)
        res  = requests.post(url=url_awvs,data=data,headers=header_awvs,verify=False)
        taskInfo[address] = res.json()["target_id"]                  #json格式化,不然,无法正常提取
        data = {"scan_speed":speed}
        data=json.dumps(data)
        #print(url_awvs+'/'+res.json()["target_id"]+"/configuration")
        res = requests.patch(url_awvs+'/'+res.json()["target_id"]+"/configuration",data=data,headers=header_awvs,verify=False)
        #print(res.text)
        # msg  = "[{current_time}] {address} {speed} 成功添加到扫描器中!".format(current_time=current_time,address=address,speed=speed)
        # print(msg)
        return True
    except Exception as e:
        # msg = "[{current_time}] {address} 未能成功添加到扫描器中,请检查原因".format(current_time=current_time,address=address)
        # print(msg)
        # print(e)
        return False

#开启扫描task_id是创建任务之后每个任务都有一个唯一的task_id,profile_id参数控制扫描类型共有H,W,C,X,S,F,speed参数控制扫描速度,共有S[slow]M[moderate]F[fast]参数
def start_scan(address,level,start_date,speed):
    start_time = start_date                         
    # day        = time.strftime("%Y-%m-%d",time.localtime())          #类似2019-01-02的时间格式
    # s          = start_time.split("T")
    # s          = s[1]
    #start_time = " " + str(day) + " " + str(s[0]) + str(s[1]) + str(":") + str(s[2]) + str(s[3]) + str(":") + str(s[4]) + str(s[5]) #转化为标准时间格式  2019-09-01 12:12:11
    start_time = awvs2standardTime(start_time)  #转化为标准时间格式  2019-09-01 12:12:11
    start_time = str(start_time["year"])+"-"+str(start_time["month"])+"-"+str(start_time["day"])+" "+str(start_time["hour"])+":"+str(start_time["minute"])+":"+str(start_time["second"])
    speed_show = scan_speed[speed]              #输入的时候是简称,但是显示的时候显全称
    level_show = profile_show[level]            #输入的时候是简称,但是显示的时候是全称
    try:
        current_time = time.strftime("%X",time.localtime())
        target_id    = taskInfo[address]                                                    #此时的target_id是添加任务时的target_id,并不是最终的target_id,但是需要target_id获取最终的target_id
        profile_id   = profile[level]
        url_awvs     = str(host_awvs)+"/api/v1/scans"                                       #设定2019-07-12  17-20点开始
        data         = {"target_id":target_id,"profile_id":profile_id,"schedule":{"disable":False,"start_date":start_date,"time_sensitive":True}}
        data         = json.dumps(data)  #
        res          = requests.post(url=url_awvs,data=data,headers=header_awvs,verify=False)
        target_id    = res.json()["target_id"]                                              #此时的target_id是最终的target_id,    
        if add_tasks(address,address,10,speed) == True:                                     #判断是否添加任务成功
            tool.print2sheet(15,address,"URL",6,start_time,"Start Time",7,level_show,"Profile",2,speed_show,"Speed",20,target_id,"ID")
        else:
            tool.print2sheet(15,address,"URL",6,start_time,"Start Time",7,level_show,"Profile",2,speed_show,"Speed",20,"目标URL未能成功添加进AWVS扫描器中,请手工检查原因","ID",color="red")
        # msg = "[{current_time}] {address}  成功开始扫描!".format(current_time=current_time,address=address)
        # print(msg)
    except Exception as e:
        tool.print2sheet(15,address,"URL",6,start_time,"Start Time",7,level_show,"Profile",2,speed_show,"Speed",20,"目标URL未能成功添加进AWVS扫描器中,请手工检查原因","ID",color="red")

#删除没有发现漏洞的任务,四个选型 1(删除没有发现任何漏洞的扫描),2(删除没有发现任何漏洞以及仅仅发现中危以下的漏洞),3(删除没有发现任何漏洞以及仅仅发现中危以下的漏洞)4(删除所有的扫描任务)
def deleteTask(types):
    types  = int(types)
    sql_0  = "SELECT target_id  FROM target_vulns_stats "                                                                      #查询有发现任何漏洞的扫描
    sql_1  = "SELECT target_id  FROM target_vulns_stats where vuln_stats[1]!=0 "                                               #查询所有发现高危的扫描任务
    sql_2  = "SELECT target_id  FROM target_vulns_stats where vuln_stats[1]=0 and vuln_stats[2]!=0 "                           #查询高危以下漏洞(不包括高危)
    sql_3  = "SELECT target_id  FROM target_vulns_stats where vuln_stats[1]=0 and vuln_stats[2]=0 and vuln_stats[2]=0 "        #查询中危以下漏洞(不包括中危)
    sql    = "SELECT address,  target_id  FROM targets where target_id "                                                       #查询url和target_id
    sql1   =  sql + "  not in ({sql_0});".format(sql_0=sql_0)                                                                  #查询没有发现任何漏洞的扫描
    sql2   =  sql + "  not in ({sql_0})".format(sql_0=sql_0)+" union " +sql + "in ({sql_3});".format(sql_3=sql_3)              #查询没有发现任何漏洞或者仅仅发现低危漏洞的扫描
    sql3   =  sql + "  not in ({sql_0})".format(sql_0=sql_0)+" union " +sql + "in ({sql_2});".format(sql_2=sql_2)              #查询没有发现任何漏洞或者仅仅发现中危及以下漏洞的扫描
    sql4   = "SELECT address,  target_id  FROM targets;"                                                                       #查询所有的url和target_id
    global taskInfo,scan_speed,url_awvs
    #task_list = tool.content2List(add)                           #读取存放任务URL和ID的txt文件
    #url      = "https://49.234.98.25:13443/api/v1/targets/065a2018-293b-4792-b9d8-fbd511b56402"
    task_url_id = []
    if  types  == 1:
        task_url_id = excuteSQL(sql1)
    elif types == 2:
        task_url_id = excuteSQL(sql2)
    elif types == 3:
        task_url_id = excuteSQL(sql3)
    elif types == 4:
        task_url_id = excuteSQL(sql4)
    for task in task_url_id: #数据库中查询URL和ID结果保存在一个数组之中
        address  = task[0]
        id       = task[1]
        url      = host_awvs+str("api/v1/targets/")+str(id)
        try:
            res     = requests.delete(url=url,headers=header_awvs,verify=False)
            if 200 == int(res.status_code):
                tool.print2sheet(15,address,"URL",18,id,"ID",20,"目标URL已经成功删除!","Status")
            else:
                tool.print2sheet(15,address,"URL",18,id,"ID",20,"目标URL未能成功删除或者已经删除,请手工检查原因!","Status",color='red')       
            pass
        except :
            tool.print2sheet(15,address,"URL",18,id,"ID",20,"目标URL未能成功删除或者已经删除,请手工检查原因!","Status",color='red')
            pass   
#读取文件内容为一个列表
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
#执行SQL语句并返回查询的结果
def  excuteSQL(SQL):
    global host,port,database,user,password
    try:
        connect = psycopg2.connect(database=database,user=user,password=password,host=host,port=port)   #连接数据库
        cur     = connect.cursor()
        cur.execute(SQL)
        rows    = cur.fetchall()
        connect.commit()
        cur.close()
        connect.close()
        return rows
        pass
    except:
        msg    = "[1] 请查看./find/module/awvs.py文件中"
        print(msg)
        msg    = "[2] #######  AWVS 相关配置信息区   #######信息是否正确"
        print(msg)
        msg    = "[3] 并确保您的awvs配置中允许远程数据库连接"
        print(msg)
        pass
    
if __name__=='__main__':     
    for address in content2List(add):         
        if "https"  not  in  address and "http"  not  in  address :             
            address ="https://"+ str(address)         
        add_tasks(address,address,"10",speed)
        start_scan(address,"H","20190724T122000+0800",'f')         
        time.sleep(5)    
