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


当你的测试用例需要验证的环境比较多时，可以并行地执行这些用例进而缩短测试总耗时。

并行的能力需要借助编程语言的多线程技术。

Grid可以根据用例中指定的平台配置信息把用例转发给符合匹配要求的测试代理。例如，你的用例中指定了要在Linux上用Firefox版本进行测试，那么Grid会自动匹配注册信息为Linux且安装了Firefox的代理节点，如果匹配成功，则转发测试请求，如果匹配失败则拒绝请求。

## 9.3 Remote应用

我们指定WebDriver支持多浏览器下的执行，这是因为WebDriver针对每一种浏览驱动都重写WebDriver方法。所以，在脚本运行之前需要先确定浏览器驱动：

    driver = webdriver.Firefox()

    driver = webdriver.Chrome()

    driver = webdriver.Ie()

### 9.3.1 WebDriver驱动分析

查看其中任何一个驱动的目录发现都有一个webdriver.py文件，除了我们熟悉的Firefox、Chrome、IE等驱动外，其中还包括非常重要的remote。从这个角度看，也可以把它看作是一种驱动类型，而这种驱动类型比较特别，它不是支持某一款特定的浏览器或平台，而是一种配置模式，我们在这种配置模式下指定任意的平台或浏览器，这种模式的执行都需要Selenium Server的支持。

打开selenium包下的webdriver/firefox目录，先看Firefox中webdriver.py文件的实现

    from .firefox_binary import FirefoxBinary
    from selenium.webdriver.firefox.firefox_profiel import FirefoxProfile
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

    class WebDriver(RemoteWebDriver):

        # There is no native event support on Mac
        NATIVE_EVENTS_ALLOWED = sys.platform != "darwin"
        
        def __init__(self, firefox_profile=None, firefox_binary=None, timeout=30,
                    capabilities=None, executable_path="wires"):

            self.binary = firefox_binary
            self.profile = firefox_profile

主机查看WebDriver类的__init__()初始化方法，因为Selenium自带Firefox浏览器驱动，所以，这个驱动的重要配置在于firefox_profile和firefox_binary两个参数。而这两个参数分别调用当前目录下的firefox_binary.py和firefox_profile.py文件

我们在脚本中调用Firefox浏览器驱动时的路径为：selenium.webdriver.Firefox()，那么它是如何指向../selenium/webdirver/firefox/webdriver.py文件中WebDriver类的呢？密码在于../selenium/webdriver/目录下的__init__.py文件。

    ...
    from .firefox.webdriver import WebDriver as Firefox
    from .firefox.firefox_profile import FirefoxProfile 
    ...

通过查看该文件就明白了它的原理，它其实对不同驱动的路径做了简化，并且将不同目录下的WebDriver类重命名为相应的浏览器（Firefox、Chrome、IE等），所以，在调用不同浏览器的驱动时就简化了层级。

再打开selenium包下的webdriver/chrome目录，查看Chrome中webdriver.py文件的实现

    ...
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver 
    ...

    class WebDriver(RemoteWebDriver):
        """
        Controls the ChromeDriver and allows you to drive the browser


        you will need to download the ChromeDriver executable from
        http://chromedriver.storage.googleapis.com/index.html
        """               
        def __init__(self, executable_path="chromedriver", port=0,
                    chrome_options=None, service_args=None,
                    desired_capabilities=None, service_log_path=None):

        """
        Creates a new instance of the chrome dirver.

        Starts the service and then creates new instance of chrome driver.

        :Args:
        - executable_path - path to the executable. If the default is used it assumes the executable is in the $PATH
        - port - port you would like the service to run, if left as 0, a free port will be found.
        - desired_capabilities: Dictionary object with non-browser specific capabilities only, such as "proxy" or "loggingPref"
        - chrome_options: this takes an instance or ChromeOptions
        """

同样查看 WebDriver类的__init__()初始化方法，因为Selenium模块不自带chromedriver.exe驱动，所以，executable_path参数会指定chromedriver驱动。

通过查看两个文件注意到一个细节，是Firefox和Chrome的WebDriver类都继承RemoteWebDriver类，也就是remote的WebDriver类。

打开Selenium包下webdriver/remote目录下的webdriver.py文件。

    ...
    class WebDriver(object):

        """
        Controls a browser by sending commands to a remote server.
        This server is expected to be running the WebDriver wire protocol as defined
        here: http://code.google.com/p/selenium/wiki/JsonWireProtocol
        :Attributes:
        - command_executor - The command.CommandExecutor object userd to execute commands.
        - error_handler - errorhandler.ErrorHandler object userd to verify that the server did not return an error.
        - session_id - The session ID to send with every command.
        - capabilities - A dictionary of capabilities of the underlying browser for this instance's session.
        - proxy - A selenium.webdriver.common.proxy.Proxy object, to specify a proxy for the browser to use.

        def __init__(self, command_executor="http://127.0.0.1:4444/wd/hub',
            desired_capabilities=None, browser_profile=None, proxy=None,keep_alive=False):

            """
            Create a new driver that will issue commands using the wire protocol.

            :Args:
            - command_executor - Either a command.CommandExecutor object or a string that specifies the URL of a remote server to send commands to.
            - desired_capabilities - Dictionary holding predefined values for starting a browser
            - browser_profile - A selenium.webdriver.firefox.firefox_profile.FirefoxProfile object. Only used if Firefox is requested.
            """

WebDriver类的__init__()初始化方法提供了一个重要信息，即command_executor参数，它默认指向本机(127.0.0.1)的端口4444端口号，通过修改这个参数可以使其指向任意的某台主机。

除此之外，我们还需要对浏览器进行配置。浏览器的配置由desired_capabilities参数决定，这个参数的秘密在Selenium包的webdriver/common目录下的desired_capabilities.py文件中。

desired_capabilities.py

    ...
    class DesiredCapabilities(object):
    ...
        FIREFOX = {
            "browserName": "firefox",# 浏览器名
            "version": "", # 浏览器版本
            "platform": "ANY", # 测试平台（ANY表示默认平台）  
            "javascriptEnabled": True, # JavaScript启动状态
            "marionette": False, 
            # marionette是python客户端允许你远程控制基于gecko的浏览器或设备运行一个marionette服务器，包括桌面Firefox和Firefox OS。Firefox特有。
        }
    ...
        CHROME = {

            "browserName": "chrome",
            "version": "",
            "platform": "ANY",
            "javascriptEnabled": True,
        }

     ...


### 9.3.2 Remote实例

remote_ts.py

    from selenium.webdirver import Remote

    driver = Remote(command_executor="http://ip:port/wd/hub",
                    desired_capabilities={'platform': 'ANY',
                                          'browserName': 'chrome',
                                          'version': '',
                                          'javascriptEnabled': True
                                         }
                    )

    driver.get('http://www.baidu.com')
    driver.find_element_by_id("kw").send_keys("remote")
    driver.find_element_by_id("su").click()

    driver.quit()

Remote()大大增加了配置的灵活性。

### 9.3.3 参数化平台及浏览器

通过Selenium Server可以轻松地创建本地节点和远程节点。而Remote的作用就是配置测试用例在这些节点上执行，下面就通过例子来演示它们两者的组合。

    java -jar selenium-server-standalone-x.xx.x.jar -role hub

    java -jar selenium-server-standalone-x.xx.x.jar -role node -port 5555

    java -jar selenium-server-standalone-x.xx.x.jar -role node -port 5556


修改后的remote_ts.py

    from selenium.webdriver import Remote

    lists = {
            "http://ip:port/wd/hub": 'chrome',
            "http://ip:port/wd/hub": 'firefox',
            "http://ip:port/wd/hub": 'internet explorer'
            }

    for host, browser in lists.items():
        print(host, browser)
        driver = Remote(command_executor=host,
                        desired_capabilities={'platform': 'ANY',
                                              'browserName': browser,
                                              'version': '',
                                              'javascriptEnabled': True
                                             }
                        )

        driver.get("http://www.baidu.com")
        driver.find_element_by_id("kw").send_keys(browser)
        driver.find_element_by_id("su").click()
        driver.close()


首先lists字典，定义不同的主机IP、端口号及浏览器。然后，通过for循环读取lists字典中的数据作为Remote()的配置信息，从而使脚本在不同的节点及浏览器下执行。

1.启动远程node

- 本地hub主机与远程node主机之间可以用ping命令连通
- 远程主机必须安装用例执行的浏览器及驱动，并且驱动要放在环境变量path的目录下。
- 远程主机必须安装Java环境，因为需要运行Selenium Server

2.操作步骤

- 启动本地hub主机(ip:172.16.10.66)

    - java -jar selenium-server-standalone-xxx.jar -role hub     

- 启动远程node主机(ip:172.16.10.34)

    - java -jar selenium-server-standalone-xxx.jar -role node -port 5555 -hub http://172.17.10.66:4444/grid/register

- 修改远程主机的IP地址及端口号，在其上面的Firefox浏览下运行脚本。


修改remote_ts.py中的lists

    lists = {
            ...
            "http://172.16.10.34:5555/wd/hub": 'firefox'
            "http://172.16.10.66:4444/wd/hub": '自动分配node'
    }   



#### Selenium Server

- 创建.bat文件 

    java -jar D:\\selenium\selenium-server-standalone-xxx.jar -role hub

然后，在需要的时候双击启动。

- 通过VisGrid工具来启动和管理节点

### 9.4 WebDriver驱动

WebDriver所支持的平台/浏览器/模式

- Android ：： 支持脚本在Android WebView应用的测试，一般指移动端浏览器

- BlackBerry：： 支持脚本在黑莓浏览器上运行

- Firefox: 包含在Selenium 安装包中：安装后直接运行Firefox浏览器

- Chrome：chromedriver.exe：Chrome

- IE：IEDriverServer.exe:老版本IE浏览器

- Edge： MicrosoftWebDriver.exe:新版Edge

- Opera: operadriver.exe:基于ChromeDriver

- Safari：包含在Selenium Server中：苹果公司开发

- HtmlUnit：包含在Selenium Server中HtmlUnit将请求返回文档模拟成HTML，从而模拟浏览器的运行，但又非真正地启动一款浏览器执行脚本

- PhantomJS：phantomjs.exe:PhantomJS是一个拥有JavaScript API的无界面WebKit，和HtmlUnit类似，可以看做是一款无界面的浏览器


1.支撑平台

Android和BlackBerry    

2.支持浏览器

Firefox、Chrome、IE、Edge、Opera、Safari

3.支持模式

HtmlUtil和PhantomJS

>关于浏览器内核
>    浏览器最重要或者说核心的部分是“Rendering Engine”，可大概翻译为“渲染引擎”，不过我们一般习惯称其为“浏览器内核”，负责对网页语法的解释（HTML、CSS、JS）并渲染网页。
>Trident
>    IE内核：IE4~IE11
>Gecko
>    Firefox内核
>Presto
>    Opera前内核（已废弃）
>Webkit（Safari内核，Chrome内核原型）
>
>Blink
>    是开源引擎WebKit中WebCore组件的一个分支



#### 9.4.4 HtmlUnit模式

    # Java页面分析器

    java -jar selenium-server-standalone-xxx.jar

    from selenium.webdriver import Remote
    from selenium.common.exceptions import WebDriverException

    dc = {'browserName': 'htmlunit'}
    driver = Remote(command_executor='http://127.0.0.1:4000/wd/hub',
                    desired_capabilities=dc)
    driver.get()

#### 9.4.5 PhantomJS模式

    # 拥有javaScript API的无界面WebKit内核，使用前需要先下载，放到python运行路径下

    from selenium import webdriver
    from time import sleep

    driver = webdriver.PhantomJS()

    