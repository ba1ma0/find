import socket,os,threading,queue,time,re,platform
from module import printc
from module import tool as tools
#import printc
#from module import printc
try:
    import requests
except:
    msg1="\n[-] 检测到您还没有安装Python3的requests依赖包,请使用 pip install requests 安装\n"
    printc.printf(msg1,'red')
#线程锁        
lock = threading.Lock()
count  = 0  #计数
#获取操作系统信息
systeminfo = platform.platform()
#读取文件每一行并将文件内容存放在列表中
def content2List(add):
    # cwd=os.getcwd()
    dirList=[]
    # Windows 操作系统中 add=cwd+"\\dict\\directory.txt"
    # Linux 操作系统中 add=cwd+"/dict/directory.txt
    f=open(add,"rb")
    for line in f.readlines():
        dirList.append(str(line)[2:-5])
    #print("Length is:"+str(len(dirList)))
    return dirList

#判断是否访问的页面是否存在
def ifExist(res):
    symbol=["404","NOT FOUND","对不起","页面不存在","502BadGateway"]
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
#根据标题判断网站是否是可访问的
def isVisible(title):
    flag=["114网址导航","403Forbidden","NotFound","页面不存在","出错","502BadGateway","访问被拒绝","BadRequest"]
    remark=True
    count=0
    for i in flag:
        if str(i) in title:
            remark =False
            break
        # else:
        #     count=count+1
    # if count==len(flag):
    #     remark=True
    return remark

#获取子域名类
class getSubdomainNames(threading.Thread):
    def __init__(self,subdomains,domain1,protocol):
        threading.Thread.__init__(self)
        self.subdomains=subdomains
        self.domain1=domain1
        self.protocol=str(protocol)
        self.p="<title>([\W\w]*?)</title>"
        self.p1="<TITLE>([\W\w]*?)</TITLE>"
    def run(self):
        global lock,count
        domain1=self.domain1
        while not self.subdomains.empty():
            subdomain=self.subdomains.get()
            # domain=httpOrHttps(domain)+"://" +subdomain+"."+domain
            domain=httpOrHttps(self.protocol)+str("://") +str(subdomain)+"."+str(domain1)
            # print(domain)
            #lock.acquire()
            try: 
                res=requests.get(domain,timeout=4)
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
                if isVisible(title)==True:
                    if lock.acquire():
                        count=count+1
                        msg1="[+] "+tools.setStr2SameLen(30,domain)+title
                        printc.printf(msg1,'green')
                        lock.release()
                else:
                    pass
            except:
                # msg2="[-] "+domain+"不可访问"
                # printc.printf(msg2,'red')
                pass
            #lock.release()
#根据不同的类型选择不同的字典 1 subnames_school 2 subnames_gov 3 subnames_company 0 default subnames ,当然也支持用户自定义字典
def dicJudgeByInput(Input):
    if "Windows" in systeminfo:   
        if Input==1:
            return os.getcwd()+"\dict\subnames_school.txt"
        elif Input==2:
            return os.getcwd()+"\dict\subnames_gov.txt"
            #return os.getcwd().replace("module","\dict\subnames_gov.txt")
        elif Input==3:
            return os.getcwd()+"\dict\subnames_company.txt"
            #return os.getcwd().replace("module","\dict\subnames_company.txt")
        else:
            #return os.getcwd().replace("module","dict\subnames.txt")
            return os.getcwd()+"\dict\subnames.txt" 
    elif "Linux" in systeminfo:
        #print(os.getcwd())
        if Input==1:
            return os.getcwd()+"/dict/subnames_school.txt"
        elif Input==2:
            #return os.getcwd().replace("module","/dict/subnames_gov.txt")
            return os.getcwd()+"/dict/subnames_gov.txt"
        elif Input==3:
            #return os.getcwd().replace("module","/dict/subnames_company.txt")
            return os.getcwd()+"/dict/subnames_company.txt"
        else:
            #return os.getcwd().replace("module","/dict/return os.getcwd()+"/dict/subnames_school.txt"")
            return os.getcwd()+"/dict/subnames.txt"
    else:
        return Input 
#判断网站使用的是http或者https
def httpOrHttps(protocol):
    if protocol=="https":
        protocol="https"
    else:
        protocol="http"
    return protocol

#得到一个队列
def GetQueue(list):
    PortQueue = queue.Queue()
    for p in list:
        PortQueue.put(p)
    return PortQueue

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
    printc.printf(msg1,"yellow")
    printc.printf(msg2,"yellow")
if __name__=='__main__':
    getSubdomainName(300,1,"ncu.edu.cn","http")

