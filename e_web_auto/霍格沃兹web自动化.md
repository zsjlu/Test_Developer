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