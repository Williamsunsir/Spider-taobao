<img src="https://img.shields.io/badge/Selenium-3.14-red.svg">  <img src="https://img.shields.io/badge/Chrome-72.0-brightgreen.svg">  <img src="https://img.shields.io/badge/ChromeDriver-72.0-blue.svg">   <img src="https://img.shields.io/badge/mitmproxy-3.0-green.svg">

<h1>淘宝商品信息抓取</h1>
</hr>
<h2>程序介绍</h2>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2019.2月最新更新.淘宝加密繁多，切会出现多次的ip验证，需要使用selenium工具辅助完成，加入自动登录程序，滑块点击验证，中间人修改js文件，等功能。
    
<h2>Installation</h1>
1.slenium

    pip install selenium
2.mitmproxy

    pip install mitmproxy #可能会出现安装blnker失败，请使用以下命令进行安装
    pip install -f mitmproxy
    

<h2>Setting</h1>
    1.新建HTTPProxy.py文件，复制以下内容。
    
    TARGET_URL = 'https://g.alicdn.com/secdev/sufei_data/3.6.11/index.js' #这个是淘宝的index.js文件的
    INJECT_TEXT = 'Object.defineProperties(navigator,{webdriver:{get:() => false}});' #js执行文件
    
    
    def response(flow):
        if flow.request.url.startswith(TARGET_URL):
            flow.response.text = INJECT_TEXT + flow.response.text
            print('注入成功')
        if 'um.js' in flow.request.url or '115.js' in flow.request.url:
            # 屏蔽selenium检测
            flow.response.text = flow.response.text + INJECT_TEXT
            
2.配置Setting.py文件
    修改Username，Password，Host,DBName,Client信息。  

<h2>Start</h2>
1.运行mitmdump命令

    mitudump -s HTTPProxy.py -p 9000 #执行HTTPProxy文件，-p开启9000代理端口，在selenium中设置 127.0.0.1：9000代理即可。

2.执行taobao.py文件，输入自己想要爬去的商品名称。

    python taobao.py
