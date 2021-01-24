# UI自动化测试框架

## 测试框架设计思想

简介

面对复杂的业务场景，简单的录制/回放速度快，但无法适应复杂场景，通过编写
自动化脚本灵活，但工作量大且可维护性差。以往的封装技术（PO）可以适应各种
UI场景，但结构松散，无法在多项目中迁移，因此，需要一种定制测试框架，可以
弥补现有框架的缺点。

#### 框架封装思想

由于UI自动化测试框架围绕UI界面使用，因此，依旧选用PageObject设计模式
对UI及测试进行封装，同时配合Pytest单元测试将脚本能够有效的组织、连贯应用
起来，从而提高框架的可维护性和可读性。由于测试框架基于PageObject设计模式，
主要方向为PO改进，数据qudong，异常处理等，比如：

- 测试数据的数据驱动：将数据存储到外部yaml文件中，利用yaml工具进行
数据读取

- 数据步骤的数据驱动：将操作步骤释放到外部yaml文件中，利用yaml工具
对操作步骤进行读取，用专门函数解析并实现操作步骤

- 自动化异常处理机制：对元素查找模块进行封装和改进，包括如果处理弹窗

#### page_object改造

在Selenium章节，已经对PageObject进行讲解，作为通用的UI测试框架，
PageObject也可适用Appium，优点如下：

- 减少代码重复

- 提高测试用例可读性

- 提高测试用例可维护性

PO的模块关系下，所有的模块要继承BasePage，App实现启动，重启，停止等
操作，Main实现进入搜索页，进入股票页等操作

base_page模块是所有page类的父类，其中定义了公共方法，比如封装下面的
find方法后，可以让子类调用find

    from appium.webdriver.webdriver import WebDriver
    
    class BasePage:
    
        _driver:WebDriver
        
        def __init__(self, driver:WebDriver =None):
            self._driver = driver
            
        def find(self, locator, value: str =None):
            if isinstance(locator, tuple):
                return self._driver.find_element(*locator)
            else:
                return self._driver.find_element(locator, value)
                
App模块封装app的启动，重启，停止等方法，当app启动时会
进入mian页面，因此在下面的main方法要return Mian,
Mian类的定义在后面会讲解：

    from appium import webdriver
    from test_appium.page.base_page import BasePage
    from test_appium.page.main import Main
    
    class App(BasePage):
    
        _package = "com.xueqiu.android"
        _activity = ".view.WelcomeActivityAlias"
        
        def start(self):
            if self._driver is None:
                caps = {}
                caps["platformName"] = "android"                             
                caps["deviceName"] = "hogwarts"                             
                caps["appPackage"] = self._package                            
                caps["appActivity"] = self._activity                            
                caps["noReset"] = True
                
                self._driver = webdriver.Remote(
                "http://localhost:4723/wd/hub",
                caps)
                self._driver.implicitly_wait(30)
            else:
                print(self._driver)
                self._driver.start_activity(self._package, self._activity)
            return self
            
        def restart(self):
            pass
            
        def stop(self):
            pass
        
        def main(self)->Main:
            return Main(self._driver)
            
Mian模块是首页的PO，其中的方法封装了首页的重要功能，
比如下面代码中的goto_search_page封装了点击搜索并
跳转到Search页：
    
    from appium.webdriver.common.mobileby import MobileBy
    from selenium.webdriver.common.by import By
    
    from test_appium.page.base_page import BasePage
    from test_appium.page.profile import Profile
    from test_appium.page.search import Search
    
    class Main(BasePage):
        def goto_search_page(self):
            self.find(MobileBy.ID, "tv_search").click()
            return Search(self._driver)
            
        def goto_stocks(self):
            pass
            
        def goto_trade(self):
            pass
            
        def goto_message(self):
            pass

Search模块可以搜索一直股票，还可以获取股票的价格

    from appium.webdriver.common.mobileby import MobileBy
    from selenium.webdriver.remote.webdriver import WebDriver
    
    class Search:
    
        _driver: WebDriver
        
        def __init__(self, driver):
            self._driver = driver
        
        def search(self, key: str):
            self._driver.find_element(
            MobileBy.ID,
            "search_input_text"
            ).send_keys(key)
            self._driver.find_element(
            MobileBy.ID,
            "name"
            ).click()
            return self
            
        def get_price(self, key: str)->float:
            return float(self._driver.find_element(
            MobileBy.ID,
            "current_price"
            ).text)
        
最后对上述代码建立测试，新建测试模块test_search:

    import pytest
    
    from test_appium.page.app import App
    
    class TestSearch:
        def setup(self):
            self.main = App().start().main()
            
        def test_search(self):
            assert self.main.\
            goto_search_page().\
            search("alibaba").\
            get_price("BABA") > 200
            
## 测试数据的数据驱动

数据驱动就是数据的改变从而驱动自动化测试的执行，最终引起
测试结果的改变。简单来说，就是参数化的应用。数据量小的测试用例可以
使用代码的参数化来实现数据驱动，数据量大的情况下建议大家使用一种
结构化的文化来对数据进行存储，然后在测试用例中读取这些数据。

#### 参数化实现数据驱动

使用pytest提供的@pytest.mark.parametrize装饰器来进行参数化

    import pytest
    
    @pytest.mark.parametrize("key, stock_type, price", [
    ("alibaba", "BABA", 200),
    ("JD", "JD", 20)
    ])
    def test_search_data(self, key, stock_type, price):
        assert self.main.goto_search_page().\
        search(key).get_price(stock_type) > price
        
pytest会将两组测试数据自动生成两个对应的测试用例并执行，生成两条测试结果。


#### 使用YAML文件实现数据驱动

当测试数据量大的情况下，可以考虑把数据存储在结构化的文件中。从文件
中读取出代码中所需要格式的数据，传递到测试方法中执行。这里推荐大家
使用yaml类型的文件来存储测试数据。YAML以使用动态字段进行结构化，它
以数据为中心，比excel、csv、Json、XML等更适合做数据驱动。

下面建立一个data/searchdata.yml文件

    -
     - 'alibaba'            
     - 'BABA'            
     - 200 
    -
     - 'JD'            
     - 'JD'            
     - 20   
     
    # 以上代码生成[["alibaba", "BABA", 200],["JD", "JD", 20]]

将测试用例中参数化的数据改造成从searchdata.yml文件中读取：

    import pytes
    import yaml
    
    @pytest.mark.parametrize("search_key, type, price", \
    yaml.safe_load(open("../data/searchdata.yml")))
    def test_search(self, search_key, type, price):
        assert self.main.goto_search_page().\
        search(search_key).get_price(type)>price

#### 测试步骤的数据驱动

了解了测试数据驱动测试用例，那么下一步我们来学习一下测试步骤的数据
驱动。测试步骤的数据驱动就是将测试步骤封装到yaml文件中管理。当测试
步骤发生改变，只需要修改yaml文件中的配置即可。

测试步骤的数据驱动

首先对测试步骤进行封装，创建一个steps.yaml文件，代码如下：

    -by: id
     locator: tv_search
     action: click
     
上面的代码定义了一个点击元素的事件，这个元素通过id='tv_search'来
定位，定位到这个元素之后执行click()方法。下面在base_page.py文件
中定义steps()方法。

    def steps(self, path):
        with open(path) as f:
            steps: list[dict] = yaml.safe_load(f)
            element: WebElement = None
            for step in steps:
                logging.info(step)
                if "by" in step.keys():
                    element = self.find(step["by"], step["locator"])
                if "action" in step.keys():
                    action = step["action"]
                    if action == 'find':
                        pass
                    elif action == "click":
                        element.click()
                        

创建一个测试类testcase/test_dd.py

    from test_appium.page.app import App
    from test_appium.page.base import BasePage
    
    class TestDD:
        def test_dd(self):
            base = BasePage()
            base.steps("../page/steps.yaml")
            
        def test_search(self):
            App().start().main().goto_search_page().search("jd")
            
#### 测试步骤的数据驱动案例

首先对测试步骤进行封装，创建一个search.yaml文件，代码如下：

    - by: id
      locator: search_input_text                
    - action: send
      value: "{key}"          
    - by: id
      locator: name
      action: click
      
上面的代码中定义了三个步骤，第一步通过id="search_input_text"定位
到这个元素。第二步会对上面定位到的元素输入，输入的内容是一个变量，可以
在代码里对这个变量赋值。第三步完成对id='name'元素的点击操作。

在base_page.py文件中完善steps()方法，对search.yaml文件中测试步骤
的实现解析：

    import yaml
    from appium.webdriver import WebElement
    from appium.webdriver.webdriver import WebDriver
    from selenium.webdriver.common.by import By
    import logging
    
    class BasePage:
    
    _params = {} # 创建一个字典用于存储传入的参数                   
    
    def __init__(self, driver: WebDriver = None):
        self._driver = driver
    
    def steps(self, path):
        with open(path) as f:
            steps: list[dict] = yaml.safe_load(f)
            element: WebElement = None
            for step in steps:
                logging.info(step)
                if "by" in step.keys():
                    element = self.find(step["by"], step["locator"])
                if "action" in step.keys():
                    action = step["action"]
                    if action == "find":
                        pass
                    elif action == "click":
                        element.click()
                    elif action == "text":
                        element.text
                    elif action == "attribute":
                        element.get_attribute(step["value"])
                    elif action in ["send", "input"]:
                        content: str=step["value"]
                        for key in self._params.keys():
                            content=content.replace(\
                            "{%s} %key, self._params[key])
                            element.send_keys(content)        
                                        
在base_page.py文件中添加一个类变量_params={}, 用来存储传入的
数据参数。在steps()方法里面添加了新的处理elif action in ["send",
"input"]:这一段代码，用来处理输入的文本来替换Yaml文件中的{key}的
内容。

在测试用例search.py文件中改写成读取search.yaml中步骤，代码如下：

from test_appium.page.base_page import BasePage

class Search(BasePage):

    _name_locator = (MobileBy.ID, "name")
    
    def search(self, key: str):
        self._params = {}
        self._params["key"] = key
        self.steps("../page/search.yaml")
        return self
        
首先将传入的搜索值变量赋值给base_page.py中的_param类变量，然后使用
steps()方法解析../page/search.yaml路径下的yaml文件，完成测试步骤
的执行。

数据驱动的意义

- 提高代码复用率，相同的测试逻辑只需编写一条测试用例，就可以被多条测试
数据复用，提高了测试代码的复用率，同时提高了测试代码的编写效率
                         
- 异常排查效率高，测试框架依据测试数据，每条数据生成一条测试用例，用例
执行过程相互隔离。如果其中一条失败，不会影响其他的测试用例。
                         
- 代码可维护性高，清晰的测试框架利于其他测试工程师阅读，提高代码的可维护性

## 自动化异常处理机制

在UI自动化测试中，会出现各种弹出：广告窗口，升级窗口，平价窗口。弹窗
的出现，极大的干扰了自动化测试的正常流程，测试会卡死甚至退出，此时需要
对已有的page_object框架进行改造，加入弹窗处理机制

使用

查找元素前，需要检查是否有弹窗，如果出现弹窗则进行处理（点击弹窗的确定
按钮或者关闭按钮）。下面代码对函数机芯异常处理，如果出现弹窗，就会找不到
元素抛出异常，异常处理会关闭弹窗，然后继续查找元素（使用递归），通常会
维护一个黑名单（表示弹窗），以下是大概代码内容：

    logging.basicConfig(level=logging.INFO)
    _driver: WebDriver
    _black_list = [
    (By.ID, 'tv_agree'),
    (By.XPATH, '//*[@text="确定"]'),
    (By.ID, 'image_cancel'),
    (By.XPATH, '//*[@text="下次再说"]')
    ]
    _error_max = 10
    _error_count = 0
    
    _params = {}
    
    def find(self, locator, value: str = None):
        logging.info(locator)
        logging.info(value)
        
        try:
            # 寻找控件
            element = self._driver.find_element(*locator)\
            if isinstance(locator, tuple) else\
            self._driver.find_element(locator, value)
            # 如果成功，清空错误计算
            self._error_count = 0
            return element
        except Exception as e:
            # 如果次数太多，就退出异常逻辑，直接报错
            if self._error_count > self._error_max:
                raise e
            # 记录一直异常的次数    
            self._error_count += 1
            # 对黑名单里的弹框进行处理
            for element in self._black_list:
                logging.info(element)
                elements = self._driver.find_elements(*element)
                if len(elements) > 0:
                    elements[0].click()
                    # 继续寻找原来的正常控件
                    return self.find(locator, value)
            # 如果黑名单也没有，就报错                    
            logging.warn("black list no one found")
            raise e                        
        
                      
                                                                
需要注意代码中的计数器，每次执行会对异常次数进行计算，比如使用_error_count,
如果发现异常错误大于限制的次数_error_max,则抛出异常。

#### 利用装饰器改进

因为异常处理在很多方法中都会用到，所以可以使用python的装饰器或者java的
注解去让更多方法具备异常处理功能。

装饰器

    def exception_handle(fun):
        def magic(*args, **kwargs):
            instance: BasePage = args[0]
            try:
                result = fun(*args, **kwargs)
                instance._retry = 0
                return result
            except Exception as e:
                instance._retry += 1
                if instance._retry > instance._retry_max:
                    raise e
                instance.driver.implicitly_wait(0)
                for e in instance.black_list:
                    elements = instance.driver.find_elements(*e)
                    if len(elements) > 0:
                        elements[0].click()
                        instance.driver.implicitly_wait(10)
                        return fun(*args, **kwargs)
        return magic

装饰器使用

    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.support import expected_conditions
    from selenium.webdriver.support.wait import WebDriverWait
        
    @exception_handle
    def find_element(self, by, value):
        return self.driver.find_element(by, value)
        
    @exception_handle
    def find_elements(self, by, value):
        return self.driver.find_elements(by, value)
        
    @exception_handle
    def click(self, by, value):
        self.driver.find_element(by, value).click()
        
    @exception_handle
    def wait(self, locator, timeout=20):
        WebDriverWait(self.driver, timeout) \
        .until(expected_conditions.element_to_be_clickable(locator))
        
                                                                                                                                         