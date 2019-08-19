# -- coding: utf-8 --
from module import printc
try:
    import requests
except:
    msg1="[-] 您还没有安装requests依赖包,请使用 pip install requests安装"
    printc.printf(msg1,'red')
try:
    import json
except:
    msg1="[-] 您还没有安装json依赖包,请使用 pip install json安装"
    printc.printf(msg1,'red')
def get_src_name(url,page):
    headers={
            "Accept":"application/json, text/javascript, */*; q=0.01",
            'Accept-Encoding': 'gzip,deflate',
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Connection":"keep-alive",
            "Content-Length":"14",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie":"__guid=66782632.3287965366713424400.1557370637004.574; PHPSESSID=2peqmlnfbet5revgoki02d71c4; __DC_sid=66782632.465769856354124160.1557968044708.3047; test_cookie_enable=null; __DC_monitor_count=8; __DC_gid=66782632.539342110.1557370637005.1557968709132.50; __q__=1557968707901",
            "Host":"www.butian.net",
            "Origin":"https://www.butian.net",
            "Referer":"https://www.butian.net/Reward/plan",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
            "X-Requested-With":"XMLHttpRequest"}
    try:
        for p in range(1,int(page)+1):
            data={"s":1,"p":p}
            res=requests.post(url=url,data=data,headers=headers)
            content=res.content
            # print(type(content))
            # print(content)
            content=json.loads(content)
            msg1="++++++++++++++++++++++++++++++++++第{p}页++++++++++++++++++++++++++++++++++++++++++".format(p=p)
            printc.printf(msg1,'yellow')
            for i in content['data']["list"]:
                msg2="名字:"+str(i["company_name"])+"   公司ID:"+str(i["company_id"])
                printc.printf(msg2,'green')
    except:
        msg3 = "-------------------------------------好像出了一点问题----------------------------------"
        msg4 = "[+] 提示1:请您检查一下URL是否正确!现在仅支持公益SRC提取哦!直接在地址栏中复制的URL有可能不是真正的请求URL哦!您可以F12查看请求URL"
        msg5 = "[+] 提示2:请您登陆补天,F12,并且复制其中的请求头中的cookie,并且改变../scan/module/butianInfo.py文件中header中的cookie选项"
        printc.printf(msg3,'red')
        printc.printf(msg4, 'green')
        printc.printf(msg5, 'green')
        pass
# if __name__=='__main__':
#     url = "https://butian.360.cn/Reward/pub"
#     page = 10
#     get_src_name(url,page)
