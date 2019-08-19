中文说明:
========
## 注意
   因为精力有限现在只适配了Windows 10 & Python 3.7,Linux上暂时还没有适配,后期会慢慢适配,Windows上运行应该是没有问题的,在使用前,您需要做以下2步操作
### 1)找到..\find\module\awvs.py文件  
![](https://raw.githubusercontent.com/ba1ma0/images/master/find/5.png)
      在awvs.py文件的16-23行根据相关提示输入您的awvs相关信息,然后保存文件  
![](https://raw.githubusercontent.com/ba1ma0/images/master/find/3.png)

### 2)如果您的awvs部署在远程服务器上您需要简单的两步(如果您的awvs部署在本地则不需要这步)
   (1)进入 /home/acunetix/.acunetix_trial/db  (ubuntu下awvs默认安装路径)  
![](https://raw.githubusercontent.com/ba1ma0/images/master/find/3.png)
   
   (2)修改postgresql.conf文件,在文件的任意地方添加 listen_addresses = '*' 然后保存   
![](https://raw.githubusercontent.com/ba1ma0/images/master/find/6.png)
   修改pg_hba.conf文件,在文件任意地方添加      
   # TYPE  DATABASE  USER  CIDR-ADDRESS  METHOD  
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
                                                               Example
    --------------------------------------------------------------------------------------------------------------------
    python  find.py   -add C:\Users\urls.txt  -start 20190819T192043+0800  -pro https   -profile  F  -speed f  -second 1800
    python  find.py   -add C:\Users\urls.txt
    python  find.py   -delete 1
    --------------------------------------------------------------------------------------------------------------------


 1. 工具的帮助信息 python find.py -help
    ![](https://raw.githubusercontent.com/ba1ma0/images/master/find/0.png)

    
 2. 下发扫描任务  python  find.py   -add C:\Users\urls.txt  -start 20190819T192043+0800  -pro https   -profile  F  -speed f  -second 1800
	![](https://raw.githubusercontent.com/ba1ma0/images/master/find/1.png)
	
 3. 删除仅发现低危或者没有发现任何漏洞的扫描任务  python find.py  -delete 1
    ![](https://raw.githubusercontent.com/ba1ma0/images/master/find/2.png) 

 4. 验证weblogic漏洞  python find.py -weblogic  C:\target.txt
    ![](https://raw.githubusercontent.com/ba1ma0/images/master/find/4.jpg) 
