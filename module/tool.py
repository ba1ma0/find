# -- coding: utf-8 --
import socket,os,threading,queue,time,re,platform,sys,json,random,subprocess,datetime
from module import printc
try:
    import requests,telnetlib
except:
    msg1="\n[-] 检测到您还没有安装Python3的requests依赖包,请使用 pip install requests 安装\n"
    printc.printf(msg1,'red')
#线程锁        
lock = threading.Lock()
count  = 0  #计数
#获取当前操作系统的信息
systeminfo = platform.platform()
def test():
    printc.printf("124","red")

#得到一个队列
def GetQueue(list):
    PortQueue = queue.Queue(65535)
    for p in list:
        PortQueue.put(p)
    return PortQueue

#导入需要的依赖包,如果用户没有安装则提示用户安装
def importModules():
    try:
        import json
    except:
        msg1="\n[-] 检测到您还没有安装Python3的json依赖包,请使用 pip install json 安装\n"
        printc.printf(msg1,'red')
    try:
        import requests
    except:
        msg1="\n[-] 检测到您还没有安装Python3的requests依赖包,请使用 pip install requests 安装\n"
        printc.printf(msg1,'red')

#通过域名获取ip
def getIPByName(host):
    try:
        return socket.gethostbyname(host)
    except:
        return 0
        pass

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
        #dirList.append(str(line)[2:-1])
        # line = line.replace("\\n","")
        # line = line.replace("'","")
        # line = line.replace("b","")
        #dirList.append(str(line))
#将内容写入文件,并返回保存内容的文件绝对路径地址
# def write2file(content,filename=1,type="ar"):
#     current           ==  os.getcwd()                #获取当前文件夹的位置
#     name              =  str(time.strftime("%Y-%m-%d_%X",time.localtime()).replace(":","")) + ".txt"  #文件输出格式2019-07-29_134142.txt
#     #filefilename,content
#     if  filename       == 1:                                                                            #用户如果没有输出保存地址,则使用默认地址
#         filename   = str(current) + name                                                       #文件输出的绝对路径
#     elif filename      !=1:
#         if "\\" in str(filename) or "/" in str(filename) :       
#             filefilename = filename
#         else:
#             fileaddress
#     f  = open(fileaddress,type)
#     f.write(content)
#     f.write("\n")
#     f.close()
#将用户输出到命令中的内容保存至txt文件中
class Logger(object):
    def __init__(self, fileN="Default.log"):
        try:
            self.terminal = sys.stdout
            self.log = open(fileN, "w+")
        except:
            print("换个路径试一试")
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
    def flush(self):
        pass
def output(add):
    sys.stdout = Logger(add)

#存放输出文件的文件名
def address(fileName):
    root_dir    = os.getcwd()                            #程序的根目录
    address  = os.path.join(root_dir,'output',fileName)  #该出妙在不用人工判断不同平台,比如是Windows还是Linux,程序可以自己判断
    # if "Windows" in systeminfo:
    #     if ":" in add:
    #         address=add
    #     else:
    #         address = str(os.getcwd()) + "\\" + str(add)
    # elif "Linux" in systeminfo:
    #     if "/" in add:
    #          address=add
    #     else:
    #         address = str(os.getcwd()) + "/" + str(add) 
    return address
#如果存在输入文件则打印,否则不打印    
def printIfExist(address):
    if address:
        msg  =  "[*] The result file is at {add}".format(add=address)
        print(msg)

#判断是否访问的页面是否存在
def ifExist(res):
    symbol=["404","NOT FOUND","对不起"]
    p="<title>([\W\w]*?)</title>"
    for i in symbol:
        if i in re.findall(p,res)[0]:
            return False
            break
        else:
            return True
#bytes 转化为str
def bytes2str(input):
    if type(input)=="bytes":
        input=bytes.decode(input)
    return input
#删除文件中无用且重复的信息            
def delUseless(add):
    try:
        s=[]
        f=open(add,"r+")
        for i in f.readlines():
            i=i.replace("\n","") 
            s.append(i)
        f.close()
        s=list(set(s))
        with open(add,"w+") as f:
            for i in s:
                f.write(i+"\n")
            f.close()
    except:
        msg1="[-] 是不是路径输错了呢?"
        printc.printf(msg1,"red")
#将爬取的res转化为标准res.text的格式
def change2standard(res):
    try:
        if res.encoding=="ISO-8859-1":
            # res.encoding="utf-8
            result=res.text.encode(res.encoding).decode('GBK')
            #result=res.text.decode(res.encoding).encode("utf8")
        else:
            result=res.text
        return bytes2str(result)
    except:
        if res.encoding=="ISO-8859-1":
            # res.encoding="utf-8
            #result=res.text.decode(res.encoding).encode("gbk")
            result=res.text.encode(res.encoding).decode('utf8')
        else:
            result=res.text
        return bytes2str(result)


#获取子域名类
class getSubdomainNames(threading.Thread):
    def __init__(self,subdomains,domain,protocol):
        threading.Thread.__init__(self)
        self.subdomains=subdomains
        self.domain=domain
        self.protocol=protocol
        self.p="<title>([\W\w]*?)</title>"
        self.p1="<TITLE>([\W\w]*?)</TITLE>"
    def run(self):
        global lock,count
        domain=self.domain
        while not self.subdomains.empty():
            subdomain=self.subdomains.get()
            # domain=httpOrHttps(domain)+"://" +subdomain+"."+domain
            domain=httpOrHttps(self.protocol)+"://" +subdomain+"."+domain
            # print(domain)
            #lock.acquire()
            try: 
                res=requests.get(domain,timeout=2)
                result=change2standard(res)
                # print(result)
                # if ifExist(res)==True:
                if (re.findall(self.p,result)):
                    title=(re.findall(self.p,result)[0])
                elif re.findall(self.p1,result):
                    title=(re.findall(self.p1,result)[0])
                else:
                    title=' '
                title=title.replace("\n","")
                title=title.replace("\r","")
                title=title.replace("\t","")
                title=title.replace(" ",'')
                count=count+1
                msg1="[+] "+domain+"   "+title
                printc.printf(msg1,'green')
            except:
                # msg2=domain+"不可访问"
                # printc.printf(msg2,'red')
                pass
            #lock.release()
#根据不同的类型选择不同的字典 1 subnames_school 2 subnames_gov 3 subnames_company 0 default subnames ,当然也支持用户自定义字典
def dicJudgeByInput(Input):
    if "Windows" in systeminfo:
        if Input==0:
            return os.getcwd().replace("module","dict\subnames.txt")
        elif Input==1:
            return os.getcwd()+"\dict\subnames_school.txt"
        elif Input==2:
            return os.getcwd().replace("module","dict\subnames_gov.txt")
        elif Input==3:
            return os.getcwd().replace("module","dict\subnames_company.txt")
    elif "Linux" in systeminfo:
        print(os.getcwd())
        if Input==0:
            return os.getcwd().replace("module","dict/subnames.txt")
        elif Input==1:
            return os.getcwd()+"/dict/subnames_school.txt"
        elif Input==2:
            return os.getcwd().replace("module","dict/subnames_gov.txt")
        elif Input==3:
            return os.getcwd().replace("module","dict/subnames_company.txt")       
    else:
        return Input 
#判断网站使用的是http或者https
def httpOrHttps(protocol):
    if protocol=="https":
        protocol="https"
    else:
        protocol="http"
        return protocol

#将字符串设定为统一长度
def setStr2SameLen(length,string,fillStr=" "):
    if length>len(string):
        length=length-len(string)
        for i in range(length):
            string=string+fillStr
        return string
    else:
        return string
#将数据打印在表格里的表头效果如下
'''                                      >title1<
>---t1_len----<    >---t1_len----<
               URL               |      Start Time      |       Profile       |  Speed  |                    ID
---------------------------------+----------------------+---------------------+---------+------------------------------------------
https://www.baidu.com

>-------ti----------<

相关参数控制效果如图所示
'''
#t1_len 输出固定长度=2*t1_len+len(title1),title标题
def setSheetTitle(t1_len=0,title1=0,t2_len=0,title2=0,t3_len=0,title3=0,t4_len=0,title4=0,t5_len=0,title5=0,color='white'):
    #此时输出一个表格
    if t1_len!=0 and t2_len == 0:
        space_1= setStr2SameLen(t1_len,""," ")
        len1   = 2*t1_len + len(title1)
        space1 = setStr2SameLen(len1,"","-") #空白部分用"-"来填充
        msg    = space_1  +str(title1) + space_1 +str("|")
        below  = space1 + str("+")  # 输出-----------------+使其看着更像一个表格
        if color != "white":
            print(msg)
            print(below)
        else:
            printc.printf(msg,color)
            printc.printf(below,color)

    #此时输出两个表格
    elif t2_len!=0 and t3_len == 0:
        space_1 = setStr2SameLen(t1_len,""," ")
        space_2 = setStr2SameLen(t2_len,""," ")
        msg     = space_1  + str(title1) + space_1 +str("|") + space_2 + str(title2) + space_2 
        len1    = 2*t1_len + len(title1)
        space1  = setStr2SameLen(len1,"","-") + str("+")
        len2    = 2*t2_len + len(title2)
        space2  = setStr2SameLen(len2,"","-")
        below   = space1 + space2
        if color == "white":
            print(msg)
            print(below)
        else:
            printc.printf(msg,color)
            printc.printf(below,color)
    #此时输出三个表格
    elif t3_len!=0 and t4_len == 0:
        space_1 = setStr2SameLen(t1_len,""," ")
        space_2 = setStr2SameLen(t2_len,""," ")
        space_3 = setStr2SameLen(t3_len,""," ")
        # space_4 = setStr2SameLen(t4_len,""," ")
        msg     = space_1  + str(title1) + space_1 +str("|") + space_2 + str(title2) + space_2 + str("|")+ space_3 + str(title3) + space_3
        len1    = 2*t1_len + len(title1)
        space1  = setStr2SameLen(len1,"","-") + str("+")
        len2    = 2*t2_len + len(title2)
        space2  = setStr2SameLen(len2,"","-") + str("+")
        len3    = 2*t3_len + len(title3)
        space3  = setStr2SameLen(len3,"","-")
        below   = space1 + space2 + space3
        if color == "white":
            print(msg)
            print(below)
        else:
            printc.printf(msg,color)
            printc.printf(below,color)
    #此时输出四个表格
    elif t4_len!=0 and t5_len == 0:
        space_1 = setStr2SameLen(t1_len,""," ")
        space_2 = setStr2SameLen(t2_len,""," ")
        space_3 = setStr2SameLen(t3_len,""," ")
        space_4 = setStr2SameLen(t4_len,""," ")
        msg     = space_1  + str(title1) + space_1 + str("|") + space_2 + str(title2) + space_2 + str("|")+ space_3 + str(title3) + space_3 + str("|") + space_4 + str(title4) +space_4
        len1    = 2*t1_len + len(title1)
        space1  = setStr2SameLen(len1,"","-") + str("+")
        len2    = 2*t2_len + len(title2)
        space2  = setStr2SameLen(len2,"","-") + str("+")
        len3    = 2*t3_len + len(title3)
        space3  = setStr2SameLen(len3,"","-") + str("+")
        len4    = 2*t4_len + len(title4)
        space4  = setStr2SameLen(len4,"","-")
        below   = space1 + space2 + space3 +space4
        if color == "white":
            print(msg)
            print(below)
        else:
            printc.printf(msg,color)
            printc.printf(below,color)
    #此时输出五个表格
    elif t5_len!=0:
        space_1 = setStr2SameLen(t1_len,""," ")
        space_2 = setStr2SameLen(t2_len,""," ")
        space_3 = setStr2SameLen(t3_len,""," ")
        space_4 = setStr2SameLen(t4_len,""," ")
        space_5 = setStr2SameLen(t5_len,""," ")
        msg     = space_1  + str(title1) + space_1 + str("|") + space_2 + str(title2) + space_2 + str("|")+ space_3 + str(title3) + space_3 + str("|") + space_4 + str(title4) +space_4 + str("|") + space_5 + str(title5) + space_5
        len1    = 2*t1_len + len(title1)
        space1  = setStr2SameLen(len1,"","-") + str("+")
        len2    = 2*t2_len + len(title2)
        space2  = setStr2SameLen(len2,"","-") + str("+")
        len3    = 2*t3_len + len(title3)
        space3  = setStr2SameLen(len3,"","-") + str("+")
        len4    = 2*t4_len + len(title4)
        space4  = setStr2SameLen(len4,"","-") + str("+")
        len5    = 2*t5_len + len(title5)
        space5  = setStr2SameLen(len5,"","-")
        below   = space1 + space2 + space3 +space4 + space5
        if color == "white":
            print(msg)
            print(below)
        else:
            printc.printf(msg,color)
            printc.printf(below,color)

'''                                      >title1<
>---t1_len----<    >---t1_len----<
               URL               |      Start Time      |       Profile       |  Speed  |                    ID
---------------------------------+----------------------+---------------------+---------+------------------------------------------
https://www.baidu.com

>-------ti----------<

相关参数控制效果如图所示
'''
#将数据打印在一个表格里面,ti_len 参数控制表格的长度(ti_len*2+len(title)),titlei参数空控制标题的内容
def print2sheet(t1_len=0,t1=0,title1=0,t2_len=0,t2=0,title2=0,t3_len=0,t3=0,title3=0,t4_len=0,t4=0,title4=0,t5_len=0,t5=0,title5=0,color='white'):
    #此时输出一个表格,并且要与上面表格标题对齐
    if t1_len!=0 and t2_len == 0:
        len1     = 2*t1_len + len(title1)
        space_1  = setStr2SameLen(len1,t1," ") + "|"
        msg      = space_1 
        if color == "white":
            print(msg)
        else:
            printc.printf(msg,color)
    #此时输出两个表格
    elif t2_len!=0 and t3_len == 0:
        len1     = 2*t1_len + len(title1)
        space_1  = setStr2SameLen(len1,t1," ") + "|"
        len2     = 2*t2_len + len(title2)
        space_2  = setStr2SameLen(len2,t2," ") 
        msg      = space_1 + space_2
        if color == "white":
            print(msg)
        else:
            printc.printf(msg,color)
    #此时输出三个表格
    elif t3_len!=0 and t4_len == 0:
        len1     = 2*t1_len + len(title1)
        space_1  = setStr2SameLen(len1,t1," ") + "|"
        len2     = 2*t2_len + len(title2)
        space_2  = setStr2SameLen(len2,t2," ") + "|"
        len3     = 2*t3_len + len(title3)
        space_3  = setStr2SameLen(len3,t3," ") 
        msg      = space_1 + space_2 + space_3
        if color == "white":
            print(msg)
        else:
            printc.printf(msg,color)
    #此时输出四个表格
    elif t4_len!=0 and t5_len == 0:
        len1     = 2*t1_len + len(title1)
        space_1  = setStr2SameLen(len1,t1," ") + "|"
        len2     = 2*t2_len + len(title2)
        space_2  = setStr2SameLen(len2,t2," ") + "|"
        len3     = 2*t3_len + len(title3)
        space_3  = setStr2SameLen(len3,t3," ") + "|"
        len4     = 2*t4_len + len(title4)
        space_4  = setStr2SameLen(len4,t4," ") 
        msg      = space_1 + space_2 + space_3 + space_4
        if color == "white":
            print(msg)
        else:
            printc.printf(msg,color)
    #此时输出五个表格
    elif t5_len!=0:
        len1     = 2*t1_len + len(title1)
        space_1  = setStr2SameLen(len1,t1," ") + "|"
        len2     = 2*t2_len + len(title2)
        space_2  = setStr2SameLen(len2,t2," ") + "|"
        len3     = 2*t3_len + len(title3)
        space_3  = setStr2SameLen(len3,t3," ") + "|"
        len4     = 2*t4_len + len(title4)
        space_4  = setStr2SameLen(len4,t4," ") + "|"
        len5     = 2*t5_len + len(title5)
        space_5  = setStr2SameLen(len5,t5," ")
        msg      = space_1 + space_2 + space_3 + space_4 + space_5
        if color == "white":
            print(msg)
        else:
            printc.printf(msg,color)
#根据用户输入C:\targets.txt   /use/targets.txt   http://www.baidu.com   返回不同字符串或者列表  判断用户输入的是地址还是网址
#简单点讲就是根据用户输入的来决定输出结果是什么
def input2result(s):
    print(s)
    res = s
    if "http" in s:
        res = s
    elif "/"  in s:
        res = content2List(s)
    elif ":\\" in s:
        #print("当前是windows")
        res = content2List(s)
    return res
#根据ip地址判断该IP地址详细信息 例如:218.205.56.222返回结果:中国浙江杭州移动
#ip参数既可以是ip地址也可以存放ip地址的txt文件
def  findAddressByIp(ip,protocol="http"):
    ip        = input2result(ip)
    setSheetTitle(t1_len=8,title1="IP",t2_len=1,title2="API ",t3_len=10,title3="Information")
    if type(ip)  == type(""): #当参数是ip地址时
        flag       =  False #标志位,如果flag为false时一直请求
        api        = "http://ip.taobao.com/service/getIpInfo.php?ip={ip}".format(ip=ip)
        try:
            #当使用taobao接口进行查询时
            res             = json.loads(requests.get(api,timeout=4).text)
            if res['code'] == 0 and res['data'] != "":
                address     = str(res["data"]["country"]) + str(res["data"]["region"]) + res["data"]["city"] + res["data"]["isp"]  
                print2sheet(t1_len=8,t1=str(ip),title1="IP",t2_len=1,t2="Taobao",title2='API',t3_len=10,t3=address,title3='Information')
            else:
                api         = "http://ip-api.com/json/{ip}?lang=zh-CN".format(ip=ip)
                res         = json.loads(requests.get(api,timeout=4).text)
                if res['status'] == "success" and res['query'] == str(ip):#查询成功的标志
                    address     = str(res["country"]) + str(res["regionName"]) + res["isp"]  
                    print2sheet(t1_len=8,t1=str(ip),title1="IP",t2_len=1,t2="ip-api",title2='API',t3_len=10,t3=address,title3='Information')
                else:
                    print2sheet(t1_len=8,t1=str(ip),title1="IP",t2_len=1,t2="None",title2='API',t3_len=10,t3="两个接口都无发正常使用,请手工查询",title3='Information')
        except Exception as e:
                #当淘宝接口无法返回正常结果时,使用另外一个接口
                try:
                    api         = "http://ip-api.com/json/{ip}?lang=zh-CN".format(ip=ip)
                    res         = json.loads(requests.get(api,timeout=4).text)
                    if res['status'] == "success" and res['query'] == str(ip):#查询成功的标志
                        address     = str(res["country"]) + str(res["regionName"]) + res["isp"]  
                        print2sheet(t1_len=8,t1=str(ip),title1="IP",t2_len=1,t2="ip-api",title2='API',t3_len=10,t3=address,title3='Information')
                except:
                    print2sheet(t1_len=8,t1=str(ip),title1="IP",t2_len=1,t2="None",title2='API',t3_len=10,t3="两个接口都无发正常使用,请手工查询",title3='Information')
                    pass
#当参数是ip.txt时
    else: 
        for i in ip:
            api        = "http://ip.taobao.com/service/getIpInfo.php?ip={ip}".format(ip=i)
            try:
                #当使用taobao接口进行查询时
                res             = json.loads(requests.get(api,timeout=4).text)
                if res['code'] == 0 and res['data'] != "":
                    address     = str(res["data"]["country"]) + str(res["data"]["region"]) + res["data"]["city"] + res["data"]["isp"]  
                    print2sheet(t1_len=8,t1=str(i),title1="IP",t2_len=1,t2="Taobao",title2='API',t3_len=10,t3=address,title3='Information')
                else:
                    api         = "http://ip-api.com/json/{ip}?lang=zh-CN".format(ip=ip)
                    res         = json.loads(requests.get(api,timeout=4).text)
                    if res['status'] == "success" and res['query'] == str(ip):#查询成功的标志
                        address     = str(res["country"]) + str(res["regionName"]) + res["isp"]  
                        print2sheet(t1_len=8,t1=str(i),title1="IP",t2_len=1,t2="ip-api",title2='API',t3_len=10,t3=address,title3='Information')
                    else:
                        print2sheet(t1_len=8,t1=str(i),title1="IP",t2_len=1,t2="None",title2='API',t3_len=10,t3="两个接口都无发正常使用,请手工查询",title3='Information')
            except Exception as e:
                    #当淘宝接口无法返回正常结果时,使用另外一个接口
                    try:
                        api         = "http://ip-api.com/json/{ip}?lang=zh-CN".format(ip=i)
                        res         = json.loads(requests.get(api,timeout=4).text)
                        if res['status'] == "success" and res['query'] == str(i):#查询成功的标志
                            address     = str(res["country"]) + str(res["regionName"]) + res["isp"]  
                            print2sheet(t1_len=8,t1=str(i),title1="IP",t2_len=1,t2="ip-api",title2='API',t3_len=10,t3=address,title3='Information')
                    except:
                        print2sheet(t1_len=8,t1=str(i),title1="IP",t2_len=1,t2="None",title2='API',t3_len=10,t3="两个接口都无发正常使用,请手工查询",title3='Information')
                        pass



    #     except Exception as e:
#         msg  =  '''出问题了!请检查是否是以下原因
# 1.网络是够通畅
# 2.ip.txt文件只能是ip地址不能包含其他信息
#         '''
#         print(msg)
    
#有些输入不含有http协议或者https,这时需要将没有协议的url默认添上协议,有协议的则不做处理    
def setDefaultPro(protocol="http",url=""):
    res         = ''
    if "http" not in url :
        res     =   str(protocol) + "://" + url
    else:
        res     = url 
    return res
#获取子域名
def getSubdomainName(nThreads,Num,domain,protocol):
    global count
    start_time=time.time()
    add=dicJudgeByInput(Num)
    subdomains=GetQueue(content2List(add))
    ThreadList=[]
    for i in range(0, nThreads):
        t = getSubdomainNames(subdomains,domain,protocol)
        ThreadList.append(t)
    for t in ThreadList:
        t.start()
    for t in ThreadList:
        t.join()
    msg1="[+] Time cost:"+str(time.time()-start_time)+" s"
    msg2="[+] {count} Subdomains have been found".format(count=count)
    printc.printf(msg1,"green")
    printc.printf(msg2,"green")
if __name__=='__main__':
    write2file()
    # getSubdomainName(300,1,"ncu.edu.cn","http")
    #bingRequests("site:ncu.edu.cn")
    #delUseless("D:\\Github\\scan\\dict\\subnames_school.txt")

