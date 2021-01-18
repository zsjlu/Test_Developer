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
    




   