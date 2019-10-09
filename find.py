# -- coding: utf-8 --
import threading, socket,time,os,re,sys,string,platform
from module import printc,butianInfo,queue,argparse,awvs,tool
from vulnerability import weblogic_cve_2019_2729,Joomla_3_4_6_RCE
######################################全局变量区######################################
current_dir     =  str(os.getcwdb(), encoding = "utf-8")          #获取当前文件根目录绝对路径
vulnerable_list =  []                                             #存放有漏洞的主机
present_time    =  time.strftime("%Y-%m-%d %X",time.localtime())  #当前详细时间 2019-08-08 14:59:22 
present_time    =  present_time.split(" ")                        #转化为['2019-08-08', '14:59:47']
day             =  present_time[0].replace("-","")                #当前日期20190725
time_show       =  present_time[1].replace(":","")                #当前时间145947
seconds_default =  600                                            #默认间隔时间10分钟
present_awvs_time = "{day}T{time}+0800".format(day=day,time=time_show) #转为化为20190724T122000+0800
######################################全局变量区######################################
def menu():
    global vulnerable_list
    day         = time.strftime("%Y-%m-%d",time.localtime()).replace("-","")    #当前日期20190725
    start_time  = "{day}T220000+0800".format(day=day)                           #默认扫描任务是每天晚上10点
    profile     = "F"                                                           #默认是全类型漏洞扫描
    speed       = 's'                                                           #默认是慢扫描
    protocol    = "http"                                                        #默认是http
    
    parser = argparse.ArgumentParser()
#AWVS区
    parser.add_argument('-add', dest='add', help='The text file of targets                                       Example: -add url.txt')
    parser.add_argument('-pro', dest='pro', help='Protocol:https or http  Default is http                        Example: -pro https ')
    parser.add_argument('-start', dest='start', help='The starting time of scanning! Default starting time is now   Example: -start {time}'.format(time=present_awvs_time))
    parser.add_argument('-speed', dest='speed', help='Scanning speed(3 options:f,m,s) Default is s Slow scanning     Example: -speed f')
    parser.add_argument('-profile', dest='profile', help='Scaning Profile(6 options:H[High vul],W[Weak Password],C[Crawling],X[XSS],S[SQL],F[Full scan])  Default is F Full scanning')
    parser.add_argument('-delete', dest='delete', help='Delete targets 4 options:1[NO vuln targets],2[NO vuln targets+low vuln targets],3[NO vuln targets+Medium vuln targets],4[All targets]  Example: -delete 1')
    parser.add_argument('-second', dest='second', help='second    Example: -second 3600')
#vulnerability
    parser.add_argument('-weblogic', dest='weblogic', help='Example: -weblogic  /usrs/targets.txt or -weblogic 127.0.0.1')
    parser.add_argument('-joomla', dest='joomla', help='Example: -joomla  /usrs/targets.txt or -joomla 127.0.0.1')
    parser.add_argument('-o', dest='o', help='Example: -o  res.txt')
    parser.add_argument('-help', action="store_true", help='To show help information')
    options = parser.parse_args()
    #批量添加扫描任务,可以自定义时间,扫描类型,扫描速度,默认是慢速扫描,全漏洞扫描,晚上十点开始扫描
    if options.add:
        second  = seconds_default            #默认是每隔10分钟开启一个新的扫描任务,主要是防止扫描器吃不消
        add = options.add                    #存放目标站点的TXT文件
        if options.pro:
            protocol = options.pro           #目标中没有协议时
        if options.start:
            start_time = options.start       #开始扫描的时间,如果没有指定立即扫描
        if options.profile:
            profile    = options.profile     #扫描类型,默认扫描类型是全扫描
        if options.speed:
            speed      = options.speed       #扫描速度,默认是慢扫描
        if options.second:
            second    = int(options.second)
        target = tool.content2List(add)      #获取扫描的目标,并将其内容转化为列表
        tool.setSheetTitle(15,"URL",6,"Start Time",7,"Profile",2,"Speed",20,"ID") #首先打印表格的标题
        count  = 0    # 每扫描1个任务,后面任务依次类推推迟1200s扫描
        for address in target:
            url_pattern = "(\w+[:/.\w-]+\.[a-z\d]{2,3}[:\w/]*)"          #匹配有效的目标地址形如https://shbxwsb.nbhrss.gov.cn:8080/1212  或者 baidu.com
            address     = re.findall(url_pattern,address,re.S)
            if address:
                count =  count + 1
                address = address[0]
                # if "www" not in address:
                #     address = "www." + address
                if re.findall("^http",address,re.S)==[] :               #对于没有指定http或者https协议的url,默认加http头,当然也可以通过-pro参数来指定
                    address = protocol +"://"+ str(address)             #如果目标中没有协议则写入协议
                if count    != 1:
	                start_time = awvs.awvs2standardTime(start_time)     #将awvs时间转化为标准时间 并返回字典的形式{"y":"2019","m":"07","d":"12","h":"12","m":"20","s":"00"}
	                start_time = awvs.nSecondLatter(start_time,second)  #每扫描1个任务,后面任务依次类推推迟300s扫描
	                start_time = awvs.time2awvstime(start_time)         #转化为awvs能够识别的时间20190805T123640+0800
                    # print(count)
                awvs.add_tasks (address,address,"10",speed)
                awvs.start_scan(address,profile,start_time,speed)       #开启扫描
    #批量删除没有发现漏洞的目标,-delete参数后面是一个存放url和ID的txt文件
    elif options.delete:
        types = int(options.delete)                                      
        print("\n")
        if  types  == 1:
            msg = "                                开始删除扫描器中没有发现任何漏洞的扫描任务"
        elif types == 2:
            msg = "                        开始删除扫描器中没有发现任何漏洞或者仅仅发现低危漏洞的扫描任务"
        elif types == 3:
            msg = "                        开始删除扫描器中没有发现任何漏洞或者发现中危以及以下漏洞的扫描"
        elif types == 4:
            msg = "                                    开始删除扫描器中的所有扫描任务"
        print(msg)
        print("\n")
        tool.setSheetTitle(15,"URL",18,"ID",20,"Status")              #设置标题
        awvs.deleteTask(types)                                        #开始进行删除任务操作
    #vulnerability区域
    elif options.weblogic:
        msg = address  =  ''
        if options.o:
            address=tool.address(options.o)   
            tool.output(address)
        res     = tool.input2result(str(options.weblogic))

        #指定http协议时
        if options.pro:
            protocol      = str(options.pro)
            if type(res) == type([]):
                for host in res:
                    host     =  tool.setDefaultPro(protocol=protocol,url=host)
                    weblogic_cve_2019_2729.check(host)
            else:
                host     =  tool.setDefaultPro(protocol=protocol,url=res)
                weblogic_cve_2019_2729.check(host,vulnerable_list=vulnerable_list)
        #不指定时默认设定http协议
        else:
           if type(res) == type([]):
                for host in res:
                    host        =  tool.setDefaultPro(url=host)
                    msg         = "[+] Start detecting if {host} is vulnerable to CVE-2019-2729".format(host=host)
                    print(msg)
                    weblogic_cve_2019_2729.check(host)
           else:
                host            =  tool.setDefaultPro(url=res)
                msg             = "[+] Start detecting if {host} is vulnerable to CVE-2019-2729".format(host=host)
                print(msg)
                weblogic_cve_2019_2729.check(host)
        # if vulnerable_list:    
        #     msg="************** Below are vulnerable URL:******************"
        #     printc.printf(msg,'yellow')
        #     tool.printList(vulnerable_list,"green")   
        tool.printIfExist(address)
#检查joomla的RCE漏洞
    elif options.joomla:
        if options.o:
            address=tool.address(options.o)   
            tool.output(address)
        res     = tool.input2result(str(options.joomla))
        #print(res)
        #指定http协议时
        if options.pro:
            protocol      = str(options.pro)
            if type(res) == type([]):
                for host in res:
                    host     =  tool.setDefaultPro(protocol=protocol,url=host)
                    msg = "[+] Starting detect {target}".format(target=host)
                    print(msg)
                    host     =  tool.setDefaultPro(protocol=protocol,url=host)
                    command  =  Joomla_3_4_6_RCE.command(host) 
                    os.system(command)

            else:
                host     = res
                host     =  tool.setDefaultPro(protocol=protocol,url=res)
                msg      = "[+] Starting detect {target}".format(target=res)
                print(msg)
                command  =  Joomla_3_4_6_RCE.command(res) 
                os.system(command)
        else:
            if type(res) == type([]):
                for host in res:
                    host        =  tool.setDefaultPro(url=host)
                    msg = "[+] Starting detect {target}".format(target=host)
                    print(msg)
                    host     =  tool.setDefaultPro(protocol=protocol,url=host)
                    command  =  Joomla_3_4_6_RCE.command(host) 
                    os.system(command)

            else:
                host     = res
                host        =  tool.setDefaultPro(url=host)
                msg      = "[+] Starting detect {target}".format(target=res)
                print(msg)
                command  =  Joomla_3_4_6_RCE.command(res) 
                os.system(command)


    else:
        helpInfo()


def helpInfo():
    helpInformaiton = """
				 /$$$$$$$$/$$$$$$ /$$   /$$ /$$$$$$$        /$$    /$$ /$$   /$$ /$$       /$$   /$$
				| $$_____/_  $$_/| $$$ | $$| $$__  $$      | $$   | $$| $$  | $$| $$      | $$$ | $$
				| $$       | $$  | $$$$| $$| $$  \ $$      | $$   | $$| $$  | $$| $$      | $$$$| $$
				| $$$$$    | $$  | $$ $$ $$| $$  | $$      |  $$ / $$/| $$  | $$| $$      | $$ $$ $$
				| $$__/    | $$  | $$  $$$$| $$  | $$       \  $$ $$/ | $$  | $$| $$      | $$  $$$$
				| $$       | $$  | $$\  $$$| $$  | $$        \  $$$/  | $$  | $$| $$      | $$\  $$$
				| $$      /$$$$$$| $$ \  $$| $$$$$$$/         \  $/   |  $$$$$$/| $$$$$$$$| $$ \  $$
				|__/     |______/|__/  \__/|_______/           \_/     \______/ |________/|__/  \__/
                                                                                
                                                                            Author : ba1ma0
                                                                            Email  : cyber-security@qq.com
AWVS:
    -add     The text file of targets                                       Example: -add url.txt
    -pro     Protocol:https or http  Default is http                        Example: -pro https 
    -start   The starting time of scanning! Default starting time is now    Example: -start {time} 
    -speed   Scanning speed(3 options:f,m,s) Default is s Slow scanning     Example: -speed f
    -profile Scaning Profile(6 options:H[High vul],W[Weak Password],C[Crawling],X[XSS],S[SQL],F[Full scan])  Default is F Full scanning
    -delete  Delete targets 4 options:1[NO vuln targets],2[NO vuln targets+low vuln targets],3[NO vuln targets+Medium vuln targets],4[All targets]
    -second  Another scan task will start in N seconds latter   Example: -seconds 3600(which mean another new task will start 1 hour latter Default is 1200s)    -help    To show help information
    -o       Output result to file
Vulnerability:
    -weblogic To find target's weblogic vulnerability                       Example: -weblogic  /usrs/targets.txt or -weblogic 127.0.0.1
    -joomla   To find target's joomla   vulnerability                       Example: -joomla    /usrs/targets.txt or -joomla 127.0.0.1              
                                                           Example
    --------------------------------------------------------------------------------------------------------------------
    python  find.py   -add C:\\Users\\urls.txt  -start {time}  -pro http   -profile  F  -speed f  -second 1800
    python  find.py   -add C:\\Users\\urls.txt   
    python  find.py   -delete 1                                                              
    --------------------------------------------------------------------------------------------------------------------
    """.format(time=present_awvs_time)
    printc.printf(helpInformaiton,"yellow")
    # print(helpInformaiton)

if __name__=='__main__':
    # awvs_time  =  "20190724T120000+0800"
    # print(awvs_time)
    # standard   = awvs.awvs2standardTime(awvs_time)  #字典
    # print(standard)
    # future     = awvs.nSecondLatter(standard,61)
    # print(future)
    # awvs_time  = awvs.time2awvstime(future)
    # print(awvs_time)
    # start_time = "20190724T120000+0800"
    # count  = 0
    # for i in range(100000000):
    #     count  = count + 1
    #     if count % 11 == 0:
    #         start_time = awvs.awvs2standardTime(start_time)     #将awvs时间转化为标准时间 并返回字典的形式{"y":"2019","m":"07","d":"12","h":"12","m":"20","s":"00"}
    #         # print(start_time)
    #         start_time = awvs.nSecondLatter(start_time,600)     #每扫描10个任务,后面任务依次类推推迟600s扫描
    #         # print(start_time)
    #         start_time = awvs.time2awvstime(start_time)         #转化为awvs能够识别的时间20190805T123640+0800
    #         print(start_time)
    menu()
    # print(tool.input2result("https://www.baidu.com"))
    # print(tool.input2result("C:\\Users\\Ma\\Desktop\\ip.txt"))
  

