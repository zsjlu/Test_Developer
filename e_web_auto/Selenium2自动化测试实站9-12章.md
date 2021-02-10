# Selenium Grid

Grid已经集成到Selenium Server中

## 9.1 Selenium Server环境配置

1.下载Selenium Server中

http://www.seleniumhq.org/download/

通过浏览器打开页面，找到Selenium Standalone Server的介绍，单击版本号链接下载，下载完成后将得到selenium-server-standalone-xxx.jar.

2.配置Java环境

- 下载java

- 配置java环境变量

- 运行Selenium Server

        java -jar selenium-server-standalone-xxx.jar


方法一

        from selenium import selenium 

        sel = selenium("localhost", 4444, "*firefox", "http://www.baidu.com/")
        
        sel.start()        

        sel.open("/")

        sel.type("id=kw", "selenium grid")

        sel.click("id=su")

        sel.wait_for_page_to_load("30000")        

        sel.stop()

9.2 selenium Grid工作原理

Grid是用于设计帮助我们进行分布式测试的工具，其整个结构由一个hub主节点和若干个node代理节点组成。

hub用来管理各个代理节点的注册和状态信息，并且接收远程客户端代码的请求调用，然后把请求的命令再转发给代理节点来执行。

使用Grid远程执行测试的代码与直接调用Selenium Server是一样的，只是环境启动的方式不一样，需要同时启动一个hub和至少一个node。

        java -jar selenium-server-standalone-x.xx.x.jar -role hub

        java -jar selenium-server-standalone-x.xx.x.jar -role node 

上面的代码分别是启动一个hub和一个node，hub默认端口号为4444，node默认端口号为5555。

若是同一台主机上要启动多个node，则需要注意指定端口号，可以通过下面的方式来启动多个node节点。

        java -jar selenium-server-standalone-x.xx.x.jar -role node -port 5555

        java -jar selenium-server-standalone-x.xx.x.jar -role node -port 5556

        java -jar selenium-server-standalone-x.xx.x.jar -role node -port 5557                