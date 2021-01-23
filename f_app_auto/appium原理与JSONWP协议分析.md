 ## Appium原理与JsonWP协议分析
 
 ### Appium原理
 
 可以使用Java、Python编写测试脚本，通过Appium服务去驱动不通设备执行
 自动化测试。Android APP使用UiAutomator驱动程序，iOS APP使用WebDriverAgent
 驱动iOS APP，ADB用来驱动ADB Server，ChromeDriver来可以用来直接与
 AdbServer进行通讯，也可以驱动Chrome、WebView及微信小程序的运行。
 AppCrawler开源框架也是利用Appium Server的服务来完成自动化遍历测试。
 
 ### Appium源码分析
 
[appium](https://github.com/appium/appium)

克隆项目到本地，开发package.json，查看Appium的依赖。从依赖库可以看出，
Appium有非常多的依赖，它通过uiautomator2控制安卓系统。用相同的方法
找到appium-uiautomator2-driver的核心依赖appium-uiautomator2-server，
它对安卓的uiautomator进行封装，把appium-uiautomator2-server项目clone
到本地。

[appium-uiautomator2-server](https://github.com/appium/appium-uiautomator2-server)

在AppiumUiAutomator2Server.java文件

下面是启动Server的代码片段：
    
    public void startServer(){
        if(serverInstrumentation == null){
            serverInstrumentation = ServerInstrumentation.getInstance();
            Logger.info("[AppiumUiAutomator2Server]", " Starting Server");
            try{
                while(!serverInstrumentation.isServerStopped()){
                    SystemClock.sleep(1000);
                    serverInstrumentation.startServer();
                }
            }catch (SessionRemovedException e){
                       }
               }
            }

在Appium日志中，可以看出uiautomator的定位策略是strategy，在源码中
可以找到相应的代码，源码中会获取三个参数："strategy","selector",
"context"

其中使用到的定位策略，如果在项目中不能满足我们的需求，比如修改图片定位
策略、新增AI定位策略。可以在appium-uiautomator2-server项目代码中进行
开发，然后编译替换原有的APK，就可以使用新增的功能。

查看Appium目录下Uiautomator编译的APK，可以发现有两个，把自己定制的
APK替换掉

不建议使用社区版的idea对项目进行编译，可以用Android Studio进行编译，
编译完成后，再次构建，构建两个apk

## JSONWP协议分析

JSON wire protocol（JSONWP）是WebDriver开发者编写的一种通信协议。
这个通信协议是一个预定义的特殊设置，通过RESTful API暴露标准端口。Appium
不仅能够实现移动端的JSONWP，并且延伸到了Selenium的JSONWP，它能够控制
不同移动设备的行为，例如通过会话安装和卸载APP。

[JSONWP模板信息](https://w3c.github.io/webdriver)

    post /session newSession New Session
    delete /session/{session id} Delete Session
    get /satus Status
    get /session/{session id}/timeouts Get Timeouts
    post /session/{session id}/timeouts Set Timeouts
    post /session/{session id}/url Navigate To
    
可以通过访问http://localhost:4723/wd/hub/sessions，查看有哪些session：

下面使用curl命令，手工在Appium上创建一个session，然后利用这个session
发送find_element请求

    curl 'http://127.0.0.1:4723/wd/hub/session'\
    -XPOST -H "Content-Type: Application/JSON" \
    -d '{"capabilities": {value}}'
    
    session_id = $(curl 'http://127.0.0.1:4723/wd/hub/sessions'\
    | awk -F\" '{print $6}')
    
    curl "http://127.0.0.1:4723/wd/hub/session/${session_id}/element"\
    -H "Content-Type: Application/JSON"\
    -d '{"using":"id","value":"user_profile_icon"}'
    
- d表示传入的参数
- H加入请求头    

注意：创建session后，如果一分钟内不进行操作，Appium会自动关闭。

## Appium源码分析

Appium是由nodejs来实现的HTTP服务，它并不是一套全新的框架，而是将
现有的优秀的框架进行了集成，以Selenium WebDriver协议（JSONWP/
RESTful web service)统一起来，使Appium这个框架满足多方面的需求。
Appium启动自动化测试后，会在被测设备（手机）上启动一个server，监听
来自Appium Server指令。不同平台采用不同的运行和交互方式。Appium
可以创建并管理多个WebDriver Session来和不同的平台交互。

### appium框架结构

appium是由多个项目构成

appium由appium项目，以及其他的工作引擎，appium有着非常复杂的目录结构：

- bin文件夹node.js项目的可执行文件配置项。一些放到全局变量的文件存放
地址，这样你就可以在命令行下敲这个文件对应的缩写，然后执行该文件。
- docs文件夹说明文档
- lib文件夹node.js的源码文件夹
- node_modules文件夹node项目默认存放插件的目录
- test文件夹测试代码所在文件夹

其中项目中有个文件package.json,这个文件是项目的描述文件。是对项目或者
模块包的描述，里面包含许多元信息。npm install命令会根据这个文件下载
所有依赖模块。我们查看这个文件可以看到项目的dependencies

里面有模块依赖的模块和版本信息。从这里面可以看到它依赖很多driver，
比如appium-android-driver、appium-base-driver、appium-espresso-driver、
appium-ios-driver、appium-uiautomator2-driver等等。下面我们
会根据appium-uiautomator2-driver重点对android测试驱动的源码进行
分析。

appium-uiautomator2-driver

appium-uiautomator2-driver也是一个Nodejs项目，是针对Android Uiautomator2
封装的Appium driver，可称为Appium UiAutomator2的驱动程序，它是一个
针对Android设备的测试自动化框架。能够驱动原生应用、混合应用和移动web
应用程序自动执行，在模拟器和真实设备上进行测试。

appium-uiautomator2-driver依赖appium-uiautomator2-server，通过
下面的方法可以启动执行Android手机中的AndroidJUnitRunner

    Starting server
    push both src and test apks to the device and \
    execute the instrumentation tests.
    
    adb shell am instrument -w io.appium.uiautomator2.\
    server.test/androidx.test.runner.AndroidJUnitRunner
    
    注意要下载下面在对应目录下操作
    
appium-uiautomator2-server

它是一个运行在设备上的netty服务器，用来监听指令并执行UiAutomator V2
命令。它修复了之前版本的大多数问题，实现了Android系统更新的分离。

在Android Studio中打开项目之后找到AppiumUiAutomator2Server.java
这个文件，startServer()方法就是它的启动入口函数。这个函数里面调的
用了ServerInstrumentation类里面的startServer()方法。

这个startServer()方法会创建一个新的线程来处理一系列的逻辑。首先会开启
Netty服务，创建一个AndroidServer对象，然后在AndroidServer里设置
好端口并调用AppiumServlet。AppiumServlet是用于管理请求的路由，将
driver发过来的请求转发给对应Handler。Handler会调用UiAutomatorV2去
执行指定操作，操作的结果经AppiumResponse统一封装。AppiumResponse会
将操作结果返回给appium-UiAutomator2-driver，再将结果返回给客户端


AppiumServlet解析

AppiumServlet是一个典型HTTP请求的处理协议。使用AppiumServlet来管理
请求，并将driver发过来的请求转发给对应RequestHandler,它会监听下面的
URL；当URL请求过来时，AppiumServlet会对它执行相关的处理。比如查找
元素，输入，点击等操作。以register(postHandler,newFindElement("
/wd/hub/session/:sessionId/element"));为例

它会通过这三个属性"strategy"、"selector"、"context"来定位元素。

### 扩展功能

在FindElement()方法具体的提供了ById、ByAccessibilityId、ByClass、
ByXpath等方法，可以扩展这部分功能，如果将来引申出来一些功能，比如将
想要增加通过图片、通过AI来定位元素的方法，可以在上面的findElement()
方法里面添加else if(by instanceof ByAI)方法，来创建新类型ByAI并且
增加功能的实现。比如未来新增了AI来定位元素的功能，可以使用AI的插件(基于
node封装的一个插件)test.api[插件](https://github.com/testdotai/appium-classifier-plugin)

用法：
    
    driver.findElement('-custom', 'ai:cart');
    
项目构建与apk安装

完成代码的修改之后需要重新编译生成相应的apk文件，并放到Appium对应
的目录下。

项目构建

gradle->appium-uiautomator2-server-master->Task-other下

分别双击assembleServerDebug与assembleServerDebugAndroidTest
即可完成编译，编译完成会在目录下生成对应的两个apk文件。

assembleServerDebugAndroidTest.apk负责安装assembleServerDebug.apk
到设备上，开启Netty服务

assembleServerDebug.apk是服务器模块，负责监听PC端Appium发送过来的请求，
将请求发送给真正底层的UiAutomator2.

也可以通过命令来构建

    gradle clean assembleE2ETestDebug assembleE3ETestDebugAndroidTest

找到编译完成的apk

    find /usr/local/lib/node_modules/appium -name "*uiautomator*.apk"
    
将编译好的APK替换这个目录下的APK即可

客户端会传递Desired Capabilities属性配置传递给Appium Server创建一个会话，
Appium Server会调用appium-uiautomator2-driver同时将UiAutomator2 Server的
两个apk安装到测试设备上来监听Appium Server发来的请求，调用UiAutomator V2去执行
指定操作，操作结果返回给appium-uiautomator2-driver，最后返回给客户端。    

        


    
        