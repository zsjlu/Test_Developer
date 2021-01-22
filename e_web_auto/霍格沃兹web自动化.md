# web自动化测试

## selenium安装

简介：webDriver、IDE、Grid

Selenium架构

在客户端完成selenium脚本编写，将脚本传送给selenium服务器，Selenium
服务器使用浏览器驱动（driver）与浏览器（browser）进行交互。

Selenium核心组件

WebDriver使用浏览器提供的api来控制浏览器，就像用户在操作浏览器，不具有
侵入性。
IDE是Chrome和Firefox扩展插件，可以录制用户在浏览器中的操作。
Grid用于Selenium分布式，你可以在多个浏览器和操作系统运行中测试用例。

下载及安装

第一种方式

python 自带的pip工具安装

pip install selenium

第二种方式

pycharm安装

selenium支持多种浏览器，需要下载对应的浏览器版本的驱动，将浏览器驱动
位置设置到环境变量；

    from selenium import webdriver
    
    driver = webdriver.Chrome()
    driver = webdrvier.Ie()
    drvier = webdriver.Firefox()
    
#### Selenium IDE

不想多说

#### selenium测试用例编写

简介

编写测试用例的优势就是可以应对更加复杂的场景以及更加符合PageObject设计
模式，可以编写出来更加易于阅读、维护代码等。

测试用例的流程

测试用例是为了实施测试而被测试的系统提供的一组集合，这组集合包含：
测试环境、测试操作、测试用例、预期结果等。

注意：一条测试用例的最终结果只有一个：成功或失败

要素：

    1.标题：是对测试用例的描述，标题应该清楚的表达测试用例的用意
    2.步骤：对测试执行过程进行描述
    3.预期结果：提供测试执行的预期结果，预期结果一般是根据需求得出，
    如果实际结果和预期结果一致则测试通过，反之失败。
    
显式等待与隐式等待

简介

在实际工作中等待机制可以保证代码的稳定性，从而代码不会因为网速、电脑
性能等条件的约束而影响运行结果。

等待就是当运行代码时，页面的渲染速度跟不上代码的运行速度时，就需要人为
的去限制代码执行的速度，这就是等待。

在做web自动化时，一般要等待页面元素加载完成后，才能执行操作，否则会报
找不到元素等各种错误，这样就是求我们在有些场景下加等待时间。

最常见的有三种等待方式：

- 隐式等待
- 显式等待
- 强制等待

隐式等待

设置一个等待时间，轮询查找（默认0.5s）元素是否出现，如果没出现就抛出
异常。这也是最常见的等待方法。

隐式等待的作用是全局的。

self.driver.implicitly_wait

显示等待

显示等待是你在代码中定义等待一定条件发生后再进一步执行你的代码。
WebDriverWait配合该类的until()和until_not()方法，就能够根据
判断条件进行等待。程序每隔一段时间（默认为0.5s）进行条件判断，如果
条件成立，则执行下一步，否则继续等待，直到超过设置的最长时间。

当隐式等待不起作用时，就会用到显式等待。

    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions
    
    driver = webdriver.Chrome()
    WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable(By.TAG_NAME, "title"))

强制等待

强制等待，线程休眠一定时间。强制等待一般在隐式等待和显示等待都不起作用时使用。

    time.sleep(10)

#### 案例

    import time
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions
    from selenium.webdriver.support import WebDriverWait
    
    class TestHogwarts():
        def setup(self):
            self.driver = webdriver.Chrome()
            self.driver.get('https://home.testing-studio.com/')
            self.driver.implicitly_wait(5)
            
        def teardown():
            time.sleep(3)
            self.driver.quit()
            
        def test_hogwarts(self):
            # 元素定位，category_name是一个元组
            category = (By.CSS_SELECTOR, "#ember195 .category-name")
            self.driver.find_element_by_link_text('分类').click()
            WebDriverWait(self.driver, 10).until(
                expected_conditions.element_to_be_clickable(category_name)
            )
            
            self.driver.find_element("category_name).click()
            
            
## web控件定位与常见操作               

id
    
    元素的id属性
    
xpath

    find_element_by_xpath("//form[@id='form']\
    /span[@class=bg s_btn_wr']/input")
    
    nodename 选取此节点的所有子节点
    
    /        从根节点选取
    
    //       从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置。
    
    .        选取当前节点
    
    ..       选取当前节点的父节点
    
    @        选取属性  
    

css_selector

    find_element_by_css_selector('.active>a')
    
    .intro              class="intro"的所有元素
    
    #firstname          id="firstname"的所有元素
    
    a[target=_blank]    具有属性target="_blank"的所有a元素
    
    p:nth-child(2)      属于其父元素的第二个p元素
    
link
    
    find_element_by_link_text('...')
    
    find_element_by_partial_link_text('...')
    
tag_name

    find_element_by_tag_name()
    避免使用
  
class_name

    find_element_by_class_name('active')
    
#### 推荐使用

    ID > CSS > Xpath > Link > class_name > tagname
    
#### 常见操作

- 输入、点击、清除    
    
    - send_keys()
    - click()
    - clear()
    
    
- 关闭窗口、浏览器

    - close() #关闭窗口
    - quit() #关闭浏览器
        
- 获取元素属性
    
    - 元素.get_attribute('属性')
    - 元素.location #获取元素位置坐标 => {'x': 844, 'y': 181 }
    - 元素.size # 获取元素大小 => { 'height': 36, 'width': 100 }
    
- 获取网页源代码、刷新页面
    
    - driver.page_source # 获取页面源代码
    - driver.refresh() # 页面刷新
    
- 设置窗口    

    - driver.minimize_window()
    - driver.maximize_window()
    - driver.set_window_size(1000, 1000)

## web控件的交互进阶

简介

selenium中与浏览器交互就需要导入Action Chains，当需要模拟键盘or
鼠标操作时，需要使用ActionChains来处理。

Action Chains类常用于模拟鼠标的行为，比如单击，双击，拖动等行为。
当你调用ActionChains的方法时，会将所有操作按顺序存入队列，当调用
perform()方法时，队列中的事件会依次执行。

引入依赖

    from selenium.webdriver import ActionChains
    from selenium import webdriver
    
    driver = webdriver.Chrome()
    action = ActionChains(driver)
    action.send_keys()
    
点击相关操作

    action.click(on_element=None) #鼠标单击指定元素，不指定会单击鼠标当前位置
    
    action.click_and_hold(on_element=None)
    
    action.context_click(on_element=None) # 右键点击
    
    action.double_click(on_element=None)
    
    # 拖拽
    action.drag_and_drop(source, target)
    
    action.drag_and_drop_by_offset(source, xoffset, yoffset)
    
按键
    
    action.key_down(value, element=None)
    
    # 实现ctrl+c操作
    
    ActionChains(driver).key_down(Keys.CONTROL)\
    .send_keys('c').key_up(Keys.CONTROL).perform()
    
鼠标移动

    action.move_by_offset(xoffset, yoffset)
    
    action.move_to_element(to_element)
    
    action.move_to_element_with_offset(to_element, xoffset, yoffset)
    
其他

    action.release(on_element=None)
    
    action.send_keys(*keys_to_send) #向焦点元素输入值
    
    action.send_keys_to_element(element, *keys_to_send)

将之前的一系列ActionChains执行
    
    action.perform()
    
    
            
            
## 网页frame与多窗口处理           

简介

当我们要定位一个元素时，怎么都定位不到的时候就要考虑是不是浏览器内嵌
了一个frame窗口或者要找到的元素在新打开的窗口里。这时候就需要进行
frame的切换以及窗口的切换。

frame类似于在原有主html的基础上又嵌套一个html，而且嵌套的html是
独立使用，互补影响。

当打开一个页面时，光标的定位是在主页面中，如果页面是由多个frame组成的，
那么无法直接定位到具体的元素，需要切换到自己所需要的frame中，再查找
该元素。

### iframe的多种切换方式

假设一个html代码
    
    <iframe src="1.html" id="hogwarts_id" name="hogwarts_name"></iframe>

那么通过传入id、name、index以及selenium的WebElement对象来切换frame

- index: 传入整型的参数，从0开始
    
    - driver.switch_to.frame(0)
    
- id: 传入字符串的参数

    - driver.switch_to.frame("hogwarts_id") 

-  name: 传入字符串的参数

    - driver.switch_to.frame("hogwarts_name")

-  WebElement:传入selenium.webelement对象
    - driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    

### iframe切换回默认页面

    在driver.switch_to.frame()之后，如果还想操作原页面，则可以使用
    
- driver.switch_to.default_content()

### iframe多层切换

    driver.switch_to.frame("iframe1")
    
    driver.switch_to.frame("iframe2")
    
    driver.switch_to.parent_frame()
    
    driver.switch_to.parent_frame()
    
### 多窗口处理

元素有属性，浏览器的窗口其实也有属性的，只是看不到，浏览器窗口的属性
用句柄（handle）来识别。

当浏览器打开一个窗口时，如果要在新的窗口操作就需要句柄切换。人为操作
的话，可以通过眼睛看，识别不同的窗口点击切换。但是脚本没长眼睛，它不
知道你操作哪个窗口，这时候只能句柄来判断了。

## 句柄的获取

当有个多个窗口时，可用window_handles打印一下句柄：

    browser = webdriver.Chrome()
    handles = browser.window_handles
    print(handles)

    current_handle = driver.current_window_handle()
    all_handle = driver.window_handles()
    for i in all_handle:
        if i != current_handle:
            driver.switch_to.window(i)
            
## 多浏览器处理

通过对代码的改造，实现自动化脚本对多浏览器的支持。

通过传递不通的参数测试不同的浏览器，用来实现浏览器的兼容性测试。

注意：需要先将各个浏览器的驱动配置好

    import os
    from selenium import webdriver
    
    def test_browser():
        browser = os.getenv("browser").lower()
        if browser == "headless":
            driver = webdriver.PhantomJS()
        elif browser == "firefox"
            driver = webdriver.Firefox()
        else:
            driver = webdriver.Chrome()
        driver.get("https://home.testing-studio.com/")
        
    mac设置环境变量
        
        browser=firefox pytest test_hogwarts.py
        
    windows下比较特殊，要使用windows下的set来给变量赋值
    
        set browser=firefox
        
        pytest test_hogwarts.py
        
## 执行JavaScript脚本

webdriver提供了execute_script()接口来调用js代码。

执行js有两种常见：

- 一种是在页面上直接执行js
- 另一种是在某个已经定位的元素上执行js

简介

javaScript是一种脚本语言，有的场景需要使用js脚本注入辅助我们完成
selenium无法做到的事情。 

执行js

selenium 可以通过execute_script()来执行JavaScript脚本。

    - driver.execute_script:同步执行JS在当前的窗口/框架下                   
    - js脚本可以在浏览器的开发者工具->Console中进行调试
    
js的返回结果

    js = "return JSON.string(performanc.timing);"
    driver.execute_script(js)
    # 获取网页性能的响应时间，js脚本中使用return代表返回获取的结果
    
arguments传参

执行JavaScript也可以通过传参的方式去传入元素信息
  
element = driver.find_element(by, locator)
# argument[0]代表所传值element的第一个参数
driver.execute_script("argument[0].click();", element) 

## 文件上传于弹框处理   

简介

在有些场景中，是需要上传文件，而selenium是无法定位到弹出的文件框以及
网页弹出的提醒。这些都是需要特殊的方式来处理。

定义一个方法，通过execute_script执行js，js脚本中arguments[0]代表
所传值element的第一个参数，click()代表js中的点击动作，element
是传入selenium.webelement对象，也就是定位到的元素

    def click_by_js():
        element = driver.find_element(By.CSS_SELECTOR,"#js_upload_input")
        driver.execute_script("arguments[0].click();", elemet)
        
文件上传

简单的input标签上传方式要使用自动化上传不难，先定位到上传按钮，然后
send_keys把路径作为值给传进去。

    driver.find_element(By.CSS_SELECTOR， "#js_upload_input").send_keys("./hogwarts.png")

其他常用的js脚本

    # 除掉元素只读属性
    driver.execute_script("arguments[0].removeAttribute('readonly')", element)
    # 元素滚动到指定位置
    driver.execute_script(("arguments[0].scrollIntoView(true);" element))
    # 将元素属性由"none"改为"block"
    driver.execute_script(('document.querySelector("#js_upload_input").style.display="block";'))

弹窗处理 

在页面操作中有时会遇到JavaScript所生成的alert、confirm以及prompt弹框，
可以使用switch_to.alert()方法定位到。然后使用text/accept/dismiss/
send_keys等方法进行操作

- switch_to.alert(): 获取当前页面上的警告框。
- text： 返回alert/confirm/prompt中的文字信息。
- accept(): 接受现有警告框，即点击确认。
- dismiss(): 解散现有警告框，即点击取消
- send_key(keysToSend): 发送文本至警告框。keysToSend：将文本发送
至警告框

alert弹框

    alert = driver.switch_to.alert
    
    print(alert.text)
    
    alert.accept()
    
    alert.dismiss()

prompt 弹框

    alert = driver.switch_to.alert
    
    print(alert.text)
    
    alert.send_keys('selenium Alert弹出窗口输入信息')
    
    alert.accept()
    
        
        
confirm 弹框
    
    alert = driver.switch_to.alert
    
    print(alert.text)
    
    alert.accept()
    
    alert.dismiss()
    
## PageObject设计

简介

为UI页面写测试用例时（比如web页面，移动端页面），测试用例会存在大量
元素和操作细节。当UI变化时，测试用例也要跟着变化，PageObject很好
的解决了这个问题！

使用UI自动化测试工具时（包括selenium，appium等），如果无统一模式进行
规范，随着用例的增多会变得难以维护，而PageObject让自动化脚本井井有序，
将page单独维护并封装细节，可以使testcase更稳健，不需要大改大动。

使用

具体做法：把元素信息和操作细节封装到Page类中，在测试用例上调用Page
对象（PageObject），比如存在一个功能“选取相册标题”，需要为之建立函数
selectAblumWithTitle()，函数内部是操作细节findElementsWithClass('album')等；

pageobject的主要原则是提供一个简单接口，让调用者在页面上可以做任何操作，
点击页面元素，在输入框输入内容等。

不用为每个UI页面都建立一个page类，只为页面中重要的元素建立page类

pageobject的目的是通过给页面建模，从而对应用程序的使用者变得有意义：

如果你想导航到另一个页面，初始page对象应当return另一个page对象，比如
点击注册，进入注册页面，在代码中应该return Register()。如果想获取页面
信息，可以return基本类型（字符串、日期）。


建议不要在page object中放断言。应该去测page object，而不是让pageobject
自己测自己，pageobject的责任是提供页面的状态信息。这里仅用HTML描述
Page Object，这种模式哈可以用来隐藏Java swing UI细节，它可用于
所有UI框架。

## PO原则

简介

PageObject的核心思想是六大原则，掌握六大原则才可以进行PageObject
实战演练，这是PageObject的精髓所在。

selenium官方提出六大原则：

1.公共方法代表页面提供的服务
2.不要暴露页面细节
3.不要把断言和操作细节混用
4.方法可以return到新打开的页面
5.不要把整页内容都放到PO中
6.相同的行为会产生不同结果，可以封装不同结果

    test_selenium
        page
            __init__.py
            components
            base_page.py
            index.py
            login.py
            register.py
        testcase
            __init__.py
            test_index.py

BasePage是所有page object的父类，它为子类提供公共的方法，比如下面
的BasePage提供初始化driver和退出driver，代码中在base_page模块的
BasePage类中使用__init__初始方法进行初始化操作，包括driver的复用，
driver的赋值，全局等待的设置（隐式等待）等等：

    from time import sleep
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    
    class BasePage:
        def __init__(self, driver:WebDriver = None):
            if driver is None:
                self._driver = webdriver.Chrome()
                self._driver.implicitly_wait(3）
                self._driver.get(self._base_url)
            else:
                self._driver = driver
        
        def close(self):
            sleep(20)
            self._driver.quit()
            

Index是企业微信首页的page object，它存在两个方法，进入注册page object
和进入登录page object，这里return方法返回page object实现了页面跳转，
比如：goto_register方法return Register，实现从首页跳转到注册页：

    from selenium.webdriver.common.by import By
    from test_selenium.page.base_page import Basepage
    from test_selenium.page.login import Login
    from test_selenium.page.register import Register
    
    class Index(BasePage):
    
        _base_url = "https://work.weixin.qq.com/"
        
        def goto_register(self):
            self._driver.find_element(By.LINK_TEXT, "立即注册").click()
            return Register(self._driver)
            
        def goto_login(self):
            self._driver.find_element(By.LINK_TEXT,"企业登录").click()
            return Login(self._driver)
            
            
            ...
            
        test_index模块是对上述功能的测试，它独立于page类
        
        from test_selenium.page.index import Index
        
        class TestIndex:
            def setup(self):
                self.index = Index()
            
            def test_register(self):
                self.index.goto_register().register("..")
            
            ...
            
            def teardown(self):
                self.index.close()
        
            
                                                                    
                   
                       
                                           