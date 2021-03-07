# BDD框架之Lettuce入门

## 12.1 什么是BDD

相信读者或多或少听说过TDD，ATDD，BDD等概念，那么它们分别指的是什么技术？
在什么样的场景下会用到它们呢？。

1）TDD：测试驱动开发（Test-Driven Development)

测试驱动开发是敏捷开发中的一项核心实践和技术，也是一种设计方法论。TDD的原理是在开发功能
代码之前，先编写单元测试用例代码，测试代码确定需要编写什么产品代码。TDD的基本思路就是通过
测试来推动整个开发的进行，但测试驱动开发并不只是单纯的测试工作，而是把需求分析、设计和质量
控制量化的过程。TDD首先考虑使用需求（对象、功能、过程、接口等），主要是编写测试用例框架对
功能的过程和接口进行设计，而测试框架可以持续进行验证。

2）ATDD：验收测试驱动开发（Acceptance Test Driven Development)

验收测试驱动开发是一种实践。在准备实施一个功能或特性之前，团队首先需要定义出期望的质量标准和
验收细则，以明确且达到共识的验收测试计划（包含一系列测试场景）来驱动开发人员的功能开发实现
和测试人员的测试脚本开发。面向开发人员，强调如何实现系统以及如何通过验收测试。

3）BDD：行为驱动开发（Behavior Driver Development）

行为驱动开发是一种敏捷软件开发技术，它鼓励软件项目中的开发者、QA、非技术人员或商业参与者之间
的协作。主要是从用户的需求出发，强调系统行为。BDD最初由DanNorth在2003年命名，它包括验收测试
和客户测试驱动等极限编程的实践，作为对测试驱动开发的回应。

>什么是极限编程

https://baike.baidu.com/item/%E6%9E%81%E9%99%90%E7%BC%96%E7%A8%8B/4690591?fr=aladdin

极限编程方法的基本特征是：
- 增量和反复式的开发----一次小的改进跟着一个小的改进。
- 反复性，通常是自动重复的单元测试，回归测试。参见JUnit。
- 结对程序设计
- 在程序设计团队中的用户交互（在场的客户）
- 软件重构
- 共享的代码所有权
- 简单
- 反馈
- 用隐喻来组织系统
- 可以忍受的速度

>不同语言下的BDD框架

- Cucumber(Ruby) http://cucumber.io
- Jdave(Java) http://jdave.org
- Behat(PHP) http://docs.behat.org/en/v2.5
- Behave(Python) http://pythonhosted.org/behave

基于Ruby编写的Cucumber由于发展较高且比较成熟，在BDD领域有相当的知名度。
而Lettuce可以看做是Python版的Cucumber。它用于Python项目的自动化测试，
它可以执行纯文本的功能描述，一个非常有用且迷人的BDD（行为驱动开发）框架。
除官方文档外，关于Lettuce的介绍并不多，所以本章的讲解也以官方文档为基础。

Lettuce使开发和测试过程变得很容易，它有很好的可扩展性、可读性，它允许我们用户
自然语言去描述一个系统的行为，你很难想象这些描述可以自动测试你的系统。

- 【a】描述的行为。
- 【b】用Python定义步骤。
- 【c】运行并观看它失败。
- 【d】编写代码以使其通过
- 【e】运行并观看它通过。

## 12.2 安装Lettuce

Lettuce官方网址：http://Letttuce.it/.

最方便的是通过pip安装Lettuce

    pip install lettuce
    
安装好Lettuce以后，打开cmd，输入Lettuce命令；如果提示
“could not find features at \features”，说明已经安装成功。
因为还没有创建Lettuce项目，所以会出现这个提示。


## 12.3 阶乘的例子

### 12.3.1 什么是阶乘

    0！= 1
    1！= 1
    2！=2*2=2
    ...

两种实现方式

factorial.py

    # 循环实现阶乘    
    def f1(n):
        c = 1
        for i in range(n):
            i = i + 1
            c = c * i
        return c
        
    # 递归实现阶乘
    def f2(n):
        if n > 1:
            return n*f2(n-1)
        else:
            return 1
    
    if __name__ == '__main__':
        # 调用方法
        print(f1(10))
        print(f2(10))
        
### 12.3.2 编写BDD实现

- tests/features/zero.feature
  
    
    Feature: Compute factorial
        In order to play with Lettuce
        As beginners
        We'll implement factorial
      
      Scenario: Factorial of 0
        Given I have the number 0
        When  I compute its factorial
        Then  I see the number 1

翻译

    功能：计算阶乘
      为了使用lettuce
      作为初学者
      我们将实现阶乘
      
      场景：0的阶乘
        假定我有数字0
        当我计算它的阶乘
        然后，我看到了1
        
第一段为功能介绍，描述需要实现什么功能；
第二段为场景描述，也可以作为是一条测试用例，当我输入什么数据，执行了什么操作后，
预期程序应该返回什么结果。

Lettuce虽然使用了自然语言的描述，却也有语法规则。

- Feature（功能）                
- Scenario（情景）                
- Given（给定）                
- And（和）                
- When（当）                
- Then（则）    

Lettuce关键字的含义与unittest中概念的对比

Feature(功能) - test suite

Scenario(情景) - test case

Given（给定条件）- setup

When（当）- test run

Then(测) - assert             
      
    
- tests/features/steps.py

    
    from lettuce import *
    
    @step('I have the number (\d+)')
    def have_the_number(step, number):
        world.number = int(number)
        
    @step('I compute its factorial')
    def compute_its_fatorial(step):
        world.number = factorial(world.number)
        
    @step('I see the number (\d+)')
    def check_number(step, expected):
        expected = int(expected)
        assert world.number == expected, "Got %d" % world.number
        
    def factorial(number):
        number = int(number)
        if (number == 0) or (number == 1):
            return 1
        else:
            return number
    # 这个factorial是错误的方法
    
### 运行Lettuce

运行cmd，切换到tests目录下，执行“Lettuce”命令

### 12.3.3 添加测试场景

zero.feature

    Feature: Compute factorial
        In order to play with Lettuce
        As beginners
        We'll implement factorial
      
      Scenario: Factorial of 0
        Given I have the number 0
        When  I compute its factorial
        Then  I see the number 1                                            
    
      Scenario: Factorial of 1
        Given I have the number 1
        When  I compute its factorial
        Then  I see the number 1                                  
        
      Scenario: Factorial of 2
        Given I have the number 2
        When  I compute its factorial
        Then  I see the number 2
        
      Scenario: Factorial of 3
        Given I have the number 3
        When  I compute its factorial
        Then  I see the number 6 
        
再次执行，发现场景四报错了；修改steps.py中的factorial函数即可


### 12.3.4 Lettuce目录结构与执行过程

Features文件和相应的Step文件是关键。

Features文件是以feature为后缀名的文件，以Given-When-Then的方式描述了系统的场景（scenarios）
行为；Step文件为普通的Python程序文件，Feature文件中的每一个Given-When-Then
步骤在Step文件中都有对应的Python执行代码，两类文件通过正则表达式相关联。

另外注意，Feature文件一定要放在features目录下，否则会提示“could not find 
features at \features”。而Step文件可放在任意目录下都能被执行到。

## 12.4 Lettuce_webdriver 自动化测试

Lettuce_webdriver属于独立的Python第三方扩展，它支持通过Lettuce运行Selenium 
WebDriver自动化测试用例。

- 安装Lettuce

- 安装Lettuce_webdriver

https://pypi.python.org/pypi/Lettuce_webdriver

    pip install lettuce_webdriver
    
- 安装nose

nose继承自unittest，属于第三方的python单元测试框架，且容易使用。
Lettuce_webdriver的运行依赖于nose框架。

nose下载地址：https://pypi.python.org/pypi/nose/

nose同样支持pip的安装方式

    pip install nose
    
features/baidu.feature

    Feature: Baidu search test case
      Scenario: search selenium
      Given I go to "http://www.baidu.com/"
        When I fill in field with id "kw" with "selenium"
        And  I click id "su" with baidu once
        Then I should see "seleniumhq.org" within 2 second
        Then I close browser

features/support/terrain.py


    from selenium import webdriver
    from lettuce import before, world
    import lettuce_webdriver.webdriver
    
    @before.all
    def setup_browser():
        world.browser = webdriver.Firefox()
        
terrain文件配置浏览器驱动，作用于所有测试用例

在featuress上级目录输入Lettuce        

features/step_definitions/steps.py

    from lettuce import *
    from lettuce_webdriver.util import assert_false
    from lettuce_webdriver.util import AssertContextManager
    
    def input_frame(browser, attribute):
        xpath = "//input[@id='%s']" % attribute
        elems = browser.find_elements_by_xpath(xpath)
        return elems[0] if elems else False
        
    def click_button(browser, attribute):
        xpath = "//input[@id='%s']  
        elems = browser.find_elements_by_xpath(xpath)
        return elems[0] if elems else False
        
    @step('I fill in field with id "(.*?)" with "(.*?)"')
    def baidu_text(step, field_name, value):
        with AssertContextManager(step):
            text_field = input_frame(world.browser, field_name)
            text_field.clear()
            text_field.send_keys(value)
            
    @step('I click id "(.*?)" with baidu once')
    def baidu_click(step, field_name):
        with AssertContextManager(step):
            click_field = click_button(world.browser, field_name)
            click_field.click()
            
    @step('I close browser')
    def close_browser(step):
        world.browser.quit()
        
                                              

          
      
                      

                                               