# Selenium Grid

selenium grid 可以远程运行selenium test，主旨是在多个机器上并运行
selenium。一个服务端发送JSON命令给已注册的GridNodes。测试联系hub以
获得对远程浏览器实例的访问。hub有一个注册服务器列表，它提供对这些服务器
的访问，并允许控制这些实例。

当测试脚本执行时间变长，测试工作也随之加大，如何节省时间成为问题，
selenium grid可以解决多任务时间问题，使用分布式将任务分发至每个节点，
多任务分发以减轻单计算机压力，selenium grid存在如下优点：

- 所有测试的中心入口点
- 管理和控制浏览器运行的Node/环境
- 扩展
- 并行运行测试
- 跨平台的测试
- 负载平衡

环境安装

从官网下载Selenium Server(Grid)，这是一个jar包，它包含了server与
nodes：[官网](https://www.selenium.dev/downloads)

使用

grid由两个重要部分组成，Hub和Nodes

其中Hub是中介，从客户端获取指令并在Nodes上远程执行它们，Hub是发送所有
测试的中心点。Selenium Grid必须存在一个Hub用来调度Node运行，Hub
可以放到单独的机器人（CI服务器、开发人员机器）。

Nodes部署在另外一台计算机上，可以执行测试用例。selenium Grid中可以
存在多个Nodes。一个Nodes不需要与Hub或其他Nodes具有相同的平台或相同
的浏览器。比如Windows上的一个Nodes可能有提供Internet Explorer，
但在Linux或Mac只能是Chrome或者Firefox。

[Grid文档](https://github.com/SeleniumHQ/selenium/wiki/Grid2)

步骤1：开启Hub

通过下面命令启动hub，它默认监听4444端口，也可以用参数-port改变端口：

    java -jar selenium-server-standalone.jar -role hub
    
其他的配置项可以用配置文件，比如下面就指定了hubConfig.json这个配置文件：

    java -jar selenium-server-standalone.jar \
    -role hub -hubConfig hubConfig.json -debug

hubConfig.json

    {
        "prot": 4444,
        "newSessionWaitTimeout": -1,
        "servlets": [],
        "withoutServlets": [],
        "custom": {},
        "capabilityMatcher":
        "org.openqa.grid.internal.utils.DefaultCapabilityMatcher",
        "registry": "org.openqa.grid.internal.DefaultGridRegistry:,
        "throwOnCapabilityNotPresent": true,
        "cleanUpCycle": 5000,
        "role": "hub",
        "debug": false,
        "browserTimeout": 0,
        "timeout": 1800
    }        
    
步骤2：开启Nodes

依旧使用上面的jar包，启动Nodes，它会随机分配端口，一个机器上可以开多个
Nodes：
    
    java -jar selenium-server-standalone.jar -role node -hub http://localhost:4444
    
可以在-jar之前输入一些命令，这些命令会被传递给Nodes，比如：

    java -Dwebdriver.chrome.\
    driver=chromedriver.exe -jar selenium-server-standalone.jar\
    -role node -nodeConfig node1Config.json
    
Nodes也可以用json文件进行配置，包括使用何种浏览器，所在平台，最大实例数等：

node.json
   
    {            
        "capabilities":
        [
            {
                "browserName": "chrome",
                "maxInstances": 5,
                "seleniumProtocol": "WebDriver"
            }
        ],
        "proxy": "org.openqa.grid.selenium.proxy.DefaultRemoteProxy",
        "maxSession": 5,
        "port": -1,
        "register": true,
        "registerCycle": 5000,
        "hub": "http://localhost:4444",
        "nodeStatusCheckTimeout": 5000,
        "nodePolling": 5000,
        "role": "node",
        "unregisterIfStillDownAfter": 60000,
        "downPollingLimit": 2,
        "debug": false,
        "servlets": [],
        "withoutServlets": [],
        "custom": {}    
    }
    
关于-host标志的说明Hub和Nodes，如果没有指定-host标志，则默认使用
0.0.0.0。这将绑定到机器的所有公共（非环回）IPv4接口。如果有一个特殊
的网络配置或任何创建额外网络接口的组件，建议使用一个值来设置-host标志，
该值允许从不同的机器访问Hub/Nodes

案例

selenium测试用例可以单机运行，但为了执行速度与可靠性，往往选择多机
分发执行，下面使用selenium grid实现多机分发。

使用hub分行selenium测试用例，在电脑上开启hub节点：

    java -jar selenium-server-standalone-3.141.59.jar -role hub
    
开启两个node节点：

    java -jar selenium-server-standalone-3.141.59.jar\
    -role node -nodeConfig node.json
    
    java -jar selenium-server-standalone-3.141.59.jar\
    -role node -nodeConfig node.json         
    
node1节点和node2节点的配置（node.json）如下，其中指定浏览器名为chrome，
使用WebDriver协议，chromedriver要提前放入环境变量：

    {            
        "capabilities":
        [
            {
                "browserName": "chrome",
                "maxInstances": 5,
                "seleniumProtocol": "WebDriver"
            }
        ],
        "proxy": "org.openqa.grid.selenium.proxy.DefaultRemoteProxy",
        "maxSession": 5,
        "port": -1,
        "register": true,
        "registerCycle": 5000,
        "hub": "http://localhost:4444",
        "nodeStatusCheckTimeout": 5000,
        "nodePolling": 5000,
        "role": "node",
        "unregisterIfStillDownAfter": 60000,
        "downPollingLimit": 2,
        "debug": false,
        "servlets": [],
        "withoutServlets": [],
        "custom": {}    
    }
    
如果注册成功，在后面的链接中可以看到这两个node：

    http://127.0.0.1:4444/grid/console

python代码如下，首先将脚本发送给selenium hub，hub会根据DesiredCapabilities
寻找匹配的node，如果找打，就进行代码分发执行：

    from selenium.webdriver import Remote
    from selenium.webdriver import DesiredCapabilities
    
    selenium_grid_url = "http://127.0.0.1:4444/wd/hub"
    capability = DesiredCapabilities.CHROME.copy()
    for i in range(1, 5):
        driver = Remote(command_executor=selenium_grid_url,\
        desired_capabilities=capability)
        driver.get("https://www.baidu.com/")
        
代码中的capability还可以指定其他字段，具体字段内容可查看官网：

    capability['platform'] = "WINDOWS"
    capability['version'] = "10"

目前启动的hub与node是在一台主机。如果在其他主机启动node需要具备以下条件：

- hub主机与node主机处于同一网段
- node主机需要安装脚本的运行环境（Python、Selenium、浏览器及浏览器驱动）
- node主机需要安装java以运行seleniumServer

    
                    
    
        
    