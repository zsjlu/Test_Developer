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
            "marionette": False, # marionette
        }
    ...
        CHROME = {

            "browserName": "chrome",
            "version": "",
            "platform": "ANY",
            "javascriptEnabled": True,
        }

     ...


   