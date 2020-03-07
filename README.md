中文说明:
========
## 注意
   最近因为精力和时间又有点多了,所以现在不仅适配了windows上Python3环境还适配了linux,Mac上的Python3环境,而且我在别人的电脑上是可以正常运行的,一些必要的依赖包我已经封装好了,所以正常情况下在windwos和Linux上python3运行是不会有问题的,在使用前,您需要做以下2步操作  
   如果实在解决不了:  
   QQ:1058763824
## 更新 2020-03-07 18:53:23  
   (1) 每次新漏洞暴露出来之后都要写批量检测代码,每次都写实在繁琐,其实写批量检测代码原理都是一样的,所以就直接写了一个poc利用框架,当新漏洞爆发时,使用者可以将任意poc(不仅仅局限python)文件夹放在../find/vulnerability下面的文件夹即可,然后就可以让poc验证框架来进行批量检测,具体使用办法请看下面使用方法。
## 更新 2019-10-09 23:32:08  
   (1) 修复在进行weblogic漏洞验证时的一个问题  
   (2) 新增joomla漏洞验证 python3 find.py  -joomla  https://www.baidu.com  或者 python3 find.py  -joomla  /Users/play/github/test.txt
## 更新 2019-09-09
   最新适配Mac
   在Mac上适配过程中遇到了一个大坑,psycopg2在Mac上安装异常崎岖,本来很很简单的一条命令就可以解决,但是pip install psycopg2之后各种报错,我尝试了,源码编译,.whl文件安装但是均失败  
   强烈建议使用anaconda,使用命令conda install psycopg2
### 1.找到..\find\module\awvs.py文件  
![](https://raw.githubusercontent.com/ba1ma0/images/master/find/5.png)
      在awvs.py文件的16-23行根据相关提示输入您的awvs相关信息,然后保存文件  
![](https://raw.githubusercontent.com/ba1ma0/images/master/find/3.png)

### 2 如果您的awvs部署在远程服务器上您需要简单的两步(如果您的awvs部署在本地则不需要这步)
   (1)进入 /home/acunetix/.acunetix_trial/db  (ubuntu下awvs默认安装路径)  
![](https://raw.githubusercontent.com/ba1ma0/images/master/find/4.png)
   
   (2)修改postgresql.conf文件,在文件的任意地方添加 listen_addresses = '*' 然后保存   
![](https://raw.githubusercontent.com/ba1ma0/images/master/find/6.png)
   修改pg_hba.conf文件,在文件任意地方添加      
  \# TYPE  DATABASE  USER  CIDR-ADDRESS  METHOD  
   host  all  all 0.0.0.0/0 md5 然后保存  
![](https://raw.githubusercontent.com/ba1ma0/images/master/find/7.png)
   或者您也可以参考 http://lazybios.com/2016/11/how-to-make-postgreSQL-can-be-accessed-from-remote-client/  
   如果实在解决不了:  
   QQ:1058763824
## 该工具诞生的背景:
   场景1:  
   某年某月的某一天我在某单位搬砖,在此期间该单位一直爆漏洞,我就马不停蹄地,重复地,机械地一个个验证该漏洞,但是由于该单位资产又非常多,手工测试过于耗费时间,换句话讲如果过一段时间我可能就忘记了某漏洞的利用方式,所以我就在想能不能把漏洞的验证方式做成一个集成工具,我只要结果,而把漏洞的详情封装成黑盒,我只需要输入目标站点就可以告诉我结果.漏洞验证模块就是这样诞生.  
   场景2:  
   某年某月某日忽然接到测试任务(不少于20个),时间紧任务重,需要在一天内测完,且需要提交一定数量的漏洞,手工测试是一种好方法,但是要在短时间内找出漏洞扫描器则是一种比较好的办法,批量下发漏洞扫描任务模块则这样诞生.  

工具的帮助信息如下:  

      Usage:
    AWVS:
    -add     The text file of targets                                       Example: -add url.txt
    -pro     Protocol:https or http  Default is http                        Example: -pro https
    -start   The starting time of scanning! Default starting time is now    Example: -start 20190819T192043+0800
    -speed   Scanning speed(3 options:f,m,s) Default is s Slow scanning     Example: -speed f
    -profile Scaning Profile(6 options:H[High vul],W[Weak Password],C[Crawling],X[XSS],S[SQL],F[Full scan])  Default is F Full scanning
    -delete  Delete targets 4 options:1[NO vuln targets],2[NO vuln targets+low vuln targets],3[NO vuln targets+Medium vuln targets],4[All targets]
    -second  Another scan task will start in N seconds latter   Example: -seconds 3600(which mean another new task will start 1 hour latter Default is 1200s)    -help    To show help information
    Vulnerability:
    -weblogic To find target's weblogic vulnerability                       Example: -weblogic  targets.txt or -weblogic 127.0.0.1
     AWVS:
    -add     The text file of targets                                       Example: -add url.txt
    -pro     Protocol:https or http  Default is http                        Example: -pro https
    -start   The starting time of scanning! Default starting time is now    Example: -start 20200307T185105+0800
    -speed   Scanning speed(3 options:f,m,s) Default is s Slow scanning     Example: -speed f
    -profile Scaning Profile(6 options:H[High vul],W[Weak Password],C[Crawling],X[XSS],S[SQL],F[Full scan])  Default is F Full scanning
    -delete  Delete targets 4 options:1[NO vuln targets],2[NO vuln targets+low vuln targets],3[NO vuln targets+Medium vuln targets],4[All targets]
    -second  Another scan task will start in N seconds latter   Example: -seconds 3600(which mean another new task will start 1 hour latter Default is 1200s)    -help    To show help information
    -o       Output result to file
    Vulnerability:
    -weblogic To find target's weblogic vulnerability                       Example: -weblogic  /usrs/targets.txt or -weblogic 127.0.0.1
    -joomla   To find target's joomla   vulnerability                       Example: -joomla    /usrs/targets.txt or -joomla  https://www.baidu.com
    -exploit                                                                Example: -exploit  /usrs/targets.txt or -exploit 127.0.0.1
    -command                                                                Example: -command  python2 poc.py  -p 3389  -d /web/web.xml
    -poc_add                                                                Example: -poc_add  "vulnerability,cve-2020-01-01,cve-2020-01-01.py"
    -flag                                                                   Example: -flag='Refused,No Response'
    -time_out                                                               Example: -time_out 1  Default is 2
    -vuln_name                                                              Example: -vuln_name  cve-2020-01-01 Default is NULL
    -ecology  To find target's ecology  vulnerability                       Example: -ecology   baidu.com or -ecology   /usrs/targets.txt
                                                           Example
    --------------------------------------------------------------------------------------------------------------------
    python3  find.py   -exploit  /user/targets.txt   -command="python2  cve-2020-01-01.py -d /web/web.xml" -poc_add = "vulnerability,cve-2020-01-01,cve-2020-01-01.py"
    python3  find.py   -add C:\Users\urls.txt  -start 20200307T185105+0800  -pro http   -profile  F  -speed f  -second 1800
    python3  find.py   -add C:\Users\urls.txt
    python3  find.py   -delete 1
    --------------------------------------------------------------------------------------------------------------------


 1. 工具的帮助信息 python find.py -help
    ![](https://raw.githubusercontent.com/ba1ma0/images/master/find/0.png)

    
 2. 下发扫描任务  python  find.py   -add C:\Users\urls.txt  -start 20190819T192043+0800  -pro https   -profile  F  -speed f  -second 1800
	![](https://raw.githubusercontent.com/ba1ma0/images/master/find/1.png)
	
 3. 删除仅发现低危或者没有发现任何漏洞的扫描任务  python find.py  -delete 1
    ![](https://raw.githubusercontent.com/ba1ma0/images/master/find/2.png) 

 4. 验证weblogic漏洞  python find.py -weblogic  C:\target.txt
    ![](https://raw.githubusercontent.com/ba1ma0/images/master/find/4.jpg) 
 5. 使用漏洞框架加载任意一个poc进行批量验证方法  
    (1)将POC文件夹放在/find/vulnerability文件夹下面
    ![](https://raw.githubusercontent.com/ba1ma0/images/master/find/8.png)  
    (2)使用命令即可进行批量探测```python  
      python3  find.py   -exploit /Users/ba1ma0/Desktop/targets.txt   -command="python2 CNVD-2020-10487.py  -p 8009  -f WEB-INF/web.xml"  -poc_add "vulnerability,CNVD-2020-10487,CNVD-2020-10487.py"  -vuln_name="CNVD-2020-10487" ```  
    ![](https://raw.githubusercontent.com/ba1ma0/images/master/find/9.png)
    (3)具体参数解释如下  
      ```python
此为批量攻击框架,只要按照相关参数配置,并把相关poc放到相关的文件夹下面便可进行批量探测
target   :[必须指定] 该字段要进行攻击的目标参数,这个需要根据源poc中的要求来填写。比如原poc中要求输入的参数是为127.0.0.1那么您就不能填写https://127.0.0.1 
flag     :[非必须]   该数组主要是根据poc执行之后的结果中是否含有某个字段来判断原POC执行是否成功以判断待测试站点是否存在漏洞
poc_add  :[必须指定] 该数组存储poc的相对路径信息比如poc的相对路径信息为../../find/vulnerability/cve-2020-0708,则poc_add存储的信息为["vulnerability","cve-2020-0708","cve-2020-0708"]信息
command  :[必须指定] 该字段主要存储原poc执行的命令比如原poc需要执行的命令为 python2 cve-2020-0708.py  -p 8009  -f WEB-INF/web.xml,待测试的目标不需要填写,因为工具会根据exploit参数传入的参数自动加上去
vulnerability:[非必须]该字段是字符串,主要是漏洞的名字比如 "cve-2019-01-02"
time_out :[非必须]该参数主要是控制poc执行的时间,超过一定时间如果还没有响应则可以认为测试站点不存在漏洞,默认时间是3s```

