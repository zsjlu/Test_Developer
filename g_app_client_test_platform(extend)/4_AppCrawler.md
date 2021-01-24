# 多平台自动遍历测试工具AppCrawler

AppCrawler是由霍格沃兹测试学院，思寒开源的一个项目，它是
一个基于Appium的自动遍历工具，支持android和iOS，可通过
配置设定遍历规则。

[开源项目地址](https://github.com/seveniruby/AppCrawler)

- 优点

    - 跨平台性：AppCrawler是基于Appium开发的，所以支持Android和IOS
    - 可控性：对测试的页面，控件类型的选择，测试的深度等都可自由控制
    - 可定制：可自定义操作，如输入，滑动等
- 缺点
    - 运行速度较慢：AppCrawler是基于Appium开发具备了跨平台的优点，
    但是也因为这层封装造成了运行速度相对比较慢    
    - 使用门槛高：正因为使用灵活性的问题，也造成了使用门槛的提高，
    主要基于yaml文件中使用Appium的相关技术知识进行配置，这就对
    使用者有了一定的技术要求。
    
[环境安装](https://pan.baidu.com/s/1dE0JDCH)        

AppCrawler是jar包，需要安装依赖环境:

- Java 版本： Java8
- Appium

使用命令查看帮助文档，相关参数含义和部分注解可参考帮忙文档：

    java -jar appcrawler-2.4.0-jar-with-dependencies.jar
    
使用

AppCrawler底层引擎为appium和adb等，确保安装了Appium和
adb工具： -Appium-wda-uiautomator2-adb-selenium

1.启动Appium

2.启动模拟器或真机，保证adb devices可以找到你的设备

3.用下面命令遍历一个已经安装过的APP
    
    java -jar appcrawler-2.4.0-jar-with-dependencies.jar\
    --capability "appPackage=com.xueqiu.android,\
    appActivity=.view.WelcomeActivityAlias"
    
Appcrawler默认从中心元素开始遍历，自动执行点击，滑动等
操作，同时会在当前目录生成以时间为命名的文件夹，包含数据，文件、
截图、log


配置文件

AppCrawler可以利用配置文件进行驱动，使用下面命令生成一个
配置文件demo.yml

    java -jar appcrawler.jar --demo
    
配置好demo.yml后，使用-c即可加载配置文件，-capability
指定app信息，-o指定报告输出目录

    java -jar <appcrawler.jar 路径>\
    -c example.yml
    --capability
    "appPackage=com.xueqiu.android, appActivity=.view.WelcomActivityAlias"\
    -o /tmp/xueqiu/1

注意：执行参数比配置文件优先级高

demo.yml 有以下主要功能：

- capability设置：与Appium完全一致              
- testcase: 用于启动app后的基础测试用例             
- selectedList：遍历范围设定             
- triggerActions： 特定条件触发执行动作的设置

#### capability

capability与Appium一致，具体内容可查看Appium的capability：

    capability:             
        noReset: "false"
        fullResest: "false"
        appium: "http://127.0.0.1:4723/wd/hub"
        appPackage: com.xueqiu.android
        appActivity: .view.WelcomeActivityAlias
        automationName: uiautomator2
        autoGrantPermissions: true

#### testcase

    testcase:
        name: "TesterHome AppCrawler"
        steps:
         - when:
            xpath: //*
            action: driver.swip(0.5, 0.8, 0.5, 0.2)
         - when:
            xpath: //*
            action: driver.swip(0.5, 0.2, 0.5, 0.8)
           then:
           - //*[contains(@text, '美股')]

简写形态：

- 直接使用xpath对应when里面的xpath                                      
- 直接使用action对应when里面的action

具体写法，下面的steps起那么有空格，不要省略：

    testcase:
     steps:
     - xpath: 自选
       action: click

action的动作支持：

- "": 只是截图记录                                            
- back: 后退                                           
- backApp: 回退到当前的App，默认等价于back行为可定制                                           
- monkey: 随机事件                                           
- xxx()珍惜代码                                            
- Thread.sleep(1000)                                           
- driver.swip(0.9, 0.8, 0.9, 0.5)                                           
- click：点击事件                                            
- longTap： 长按
- 除以上所有行为外均视为输入行为

正则：使用^开头的就认定为正则，比如：^确定$, ^.*输入密码


#### selectedList

selectedList可设定遍历范围，比如点击所有可点击的TextView
和ImageView控件：

    selectedList:
    - xpath: //android.widget.ImageView[@clickable='true']
    - xpath: //*[@clickable='true' and contains(@class, "Text")]


与之类似的有firstList和lastList，表示优先点击与最后点击：

- firstList：优先被点击                                                        
- lastList：最后执行

设置其最后才执行“确定”按钮，修改完成如下：

    lastList:
    - { xpath: text_yes, action: click }

#### 其他参数

- backButton: 当所有元素都被点击后默认后退控件定位                                                           
- blackList：黑名单                                                           
- triggerAction： 特定条件出发执行动作的设置                                                          
- tagLimit：自定义控件类型的点击次数                                                          
- tagLimitMax： 同类型的最多点击的次数                                                          
- assertGlobal: 设置一个全局断言，可断言当前app是否包名符合要求                                                          
- maxDepth：遍历的最大深度

#### 自动遍历过程

- 信息的获取：
    - 把当前app的界面dump为xml结构
- 获取待遍历元素
    - 遍历范围selectedList                                                             
    - 过滤黑名单、小控件、不可见控件、blackList                                                             
    - 重排控件顺序firstList lastList                                                             
    - 跳过已点击+跳过限制点击的控件tagLimit                                                             
    - 根据匹配的规则执行action循环上面的步骤
    
#### 测试报告

打开测试报告中的index.html文件，AppCrawler把每次点击
当做一个测试用例，每一个页是一个测试套件：

- Succeed：成功                                                                 
- Failed：失败                                                                
- Canceled： 发现了控件，但没有点击

AppCrawler.log记录了执行步骤（-vv 参数让log更详细），
第一项表示执行的步骤，同时会显示源码位置，选取元素的数量，
选取的元素及动作

#### 案例

案例1

    capability:
     noReset: "true"
     fullReset: "false"
     appium: "http://127.0.0.1:4723/wd/hub"
     appPackage: "com.xueqiu.android"
     appActivity: ".view.WelcomActivityAlias"
    testcase:
     steps:
     - xpath: "//*[@text='行情']"
       action: click
    selectedList:
     - xpath: "//*[contains(@resource-id,\
     'stock_index_quote_view_layout')]//*[@clickable='true']"
注意

- 可以用{}包裹需要执行的事件，元素定位符和操作action用逗号隔开。       
- xpath中直接写id或text文本信息，就会默认使用包含去查找

案例2

    capability:
     noReset: "true"
     fullReset: "false"
     appium: "http://127.0.0.1:4723/wd/hub"
     appPackage: "com.xueqiu.android"
     appActivity: ".view.WelcomActivityAlias"
    testcase:
     steps:
     - xpath: "//*[@text='行情']"
       action: click
    selectedList:
     - xpath: "//*[contains(@resource-id,\
     'quote_view_layout')]//*[@clickable='true']"
     - xpath: "//*[contains(@resource-id,\
     'id/pager')]//*[@clickable='true']"
    firstList:
     - xpath: "//*[contains(@resource-id, 'id/pager')]\
     //*[@clickable='true']"

                                                                