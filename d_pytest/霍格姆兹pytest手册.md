# python 测试框架
## python 测试框架
简介

pytest是一个成熟的全功能python测试工具，可以帮助您编写更好的程序。
它与python自带的unittest测试框架类似，但pytest使用起来更加简介高效，
并且兼容unittest框架。pytest能够支持简单的单元测试和复杂的功能测试，
pytest本身支持单元测试，可以结合requests实现接口测试，结合selenium、
appium实现自动化功能测试，使用pytest结合allure集成到Jenkins中实现
持续集成。工作中一般会使用持续集成来完成代码集成到主干分支之后的回归测试，
通过自动化测试的手段来实现产品的快速迭代，同时还能保证产品的高质量。pytest
支持315种以上的插件，可以[访问网址](http://plugincompat.herokuapp.com/),
可以[访问网址](https://docs.pytest.org)查看帮助文档

安装

    pip install -U pytest

查看版本

    pytest --version
    
 
 
##用例的识别与运行

- 测试文件以test_开头（以_test结尾也可以)
- 测试类以Test开头，并且不能带有init方法
- 测试函数以test_开头
- 断言使用基本的assert即可

在对应文件路径下执行***pytest***，它会收集符合编写规范的函数，类以及方法；
执行结果中F代表用例未通过（断言错误）， "."代表用例通过。如果有报错会有详细
的错误信息。pytest也支持unittest模式的用例定义。

####运行参数

pytest带有很多参数，可以使用pytest --help来查看帮助文档，

- 无参数

    读取路径下所有符合规则的文件，类，方法，函数全部执行。使用方法如下：

        pytest 或者 py.test
    
- -v参数

    打印详细运行日志信息，一般在调试的时候加上这个参数，终端会打印出
    每条用例的详细日志信息，方便定位问题

        pytest -v

- -s参数

    带控制台输出结果，当你的代码里面有print输出语句，如果想在运行结果
    中打印print输出的代码，在运行的时候可以添加-s参数，一般在调试的
    时候使用，使用方法如下：

        pytest -s
    
    跳过运行某个或者某些用例。应用场景：在测试场景中，开发人员有一部分
    功能代码还没实现，测试人员已经将测试用例设计出来，或者测试人员发现了
    某功能上的bug需要开发人员修复之后再测试这部分有缺陷的测试用例，
    可以将这部分测试用例在运行的时候暂时跳过，等功能实现或者bug解决之后
    再加入运行。

        pytest -k "类名"
        pytest -k "方法名"
        pytest -k "类名 and not 方法名" # 运行类里所有的方法，不包含某个方法

- -x参数

    遇到用例失败立即停止运行
    
    应用场景：在回归测试过程中，假如一共有10条基础用例，当开发人员
    打完包提交测试的时候，需要先运行这10条基础用例，全部通过才能提交
    给测试人员正式测试。如果有一条用例失败，都将这个版本打回给开发人员。
    这时就可以添加-x参数，一旦发现有失败的用例即终止运行。
    
        pytest -x
    
- --maxfail参数

    用例失败个数达到阈值停止运行
    
        pytest --maxfail=1
        
- -m参数

    将运行有@pytest.mark.[标记名]这个标记的测试用例。
    
        pytest -m 标记名  

- 运行模式

    pytest 文件名.py             
    pytest 文件名.py::类名             
    pytest 文件名.py::类名::方法名

    封装代码后通过pytest运行时报错模块没找到错误。

    导入模块前面加上这2句话解决 No modlue name '模块名'的报错。

    import os,sys                                     

    sys.path.append(os.getcwd())            #告诉pytest运行前先检索当前路径

    报错原因pytest运行时没有检索当前目录自己导入的模块

    在pycharm中运行pytest用例


    设置-》Tools-》Python Integrated Tools-》Testing:pytest
  
  
  
  
## pytest框架结构

与unittest类似，执行用例前后会执行setup，teardown来增加用例的前置和后置条件。
pytest框架中使用setup，teardown更灵活，按照用例运行级别可以分为以下几类：

- 模块级(setup_module/teardown_module)                 
- 函数级(setup_function/teardown_function)                 
- 类级(setup_class/teardown_class)                 
- 方法级(setup_method/teardown_method)                 
- 方法级(setup/teardown)                 

调用顺序

    setup_module>setup_class>setup_method>setup>teardown>teardown_method>
    teardown_class>teardown_module
    

## 控制用例的执行顺序

pytest加载所有的用例是乱序的，使用pytest.mark.run(order=[num])来设置执行顺序，
这里需要安装一个插件

安装
    
    pip install pytest-ordering
    
案例

    import pytest
    
    class TestPytest(object):
        
        @pytest.mark.run(oder=-1)
        def test_two(self):
            print("test_two.测试用例")
            
        @pytest.mark.run(order=3)
        def test_one(self):
            print("test_one, 测试用例）
            
            
##pytest fixtures

pytest中可以使用@pytest.fixture装饰器来修饰一个方法，被装饰方法的方法名可以作为一个
参数传入到测试方法中。可以使用这种方式来完成测试之前的初始化，也可以返回数据给测试函数。


将fixture作为函数参数


fixture是在测试函数运行前后，由pytest执行的外壳函数。fixture中的代码可以定制，满足多变
的测试需求，包括定义传入测试中的数据集、配置测试前系统的初始状态、为批量测试提供数据源。

@pytest.fixture()装饰的函数，可以作为参数传到执行的测试方法中执行，这样可以为这些测试
方法提供前置执行条件

    import pytest
    
    @pytest.fixture()
    def login():
        print("这是个登陆方法")
        return('tom','123')
    
    def test_casce1(login,operate):
        print(login)
        print("test_case1, 需要登陆")
        
 
指定范围内共享

fixture里面有一个参数scope, 通过scope可以控制fixture的作用范围，根据作用范围大小划分：
session>module>class>function, 具体作用范围如下：

- function函数或者方法级别都会被调用
- class类级别调用一次
- module模块级别调用一次
- session是多个文件调用一次(可以跨.py文件调用，每个.py文件都是module)

例如整个模块有多条测试用例，需要在全部用例执行之前打开浏览器，全部执行完之后去关闭浏览器，
打开和关闭操作只执行一次，如果每次都重新执行打开操作，会非常占用系统资源。这种场景除了
setup_moduel,teardown_module可以实现，还可以通过设置模块级别的fixture装饰器
@pytest.fixture(scope="module")来实现

***scope="module"***

fixture参数scope="module",module作用是整个模块都会生效,在当前.py脚本里面所有的用例
开始前只执行一次。

@pytest.fixture()如果不写参数，参数默认scope="function".

    @pytest.fixture(scope="module")
    def open():
        print("打印浏览器")
        yield
        print("执行teardown !")
        print("最后关闭浏览器")
    
    @pytest.mark.usefixtures("open")
    def test_search1():
        print("test_search1")
        raise NameError
        pass
    

scope="module"与yield结合，相当于setup_module和teardown_module方法。如果用例
出现异常，不影响yield后面的teardown执行。可以使用@pytest.mark.usefixtures装饰器
来进行方法的传入。


         
         
         
##conftest.py文件

fixture scope为session级别是可以跨.py模块调用的，也就是当我们有多个.py文件的用例时，
如果多个用例只需调用一次fixture，可以将scope="session",并且写到conftest.py文件里。
写到conftest.py文件可以全局调用这里面的方法。使用的时候不需要导入conftest.py这个文件。
使用conftest.py的规则：

- conftest.py这个文件名是固定的，不可以更改。
- conftest.py与运行用例在同一个包下，并且该包中有__init__.py文件
- 使用的时候不需要导入conftest.py，pytest会自动识别这个文件
- 放到项目的根目录下可以全局调用，放到某个package下，就在这个package内有效。

    conftest.py文件定义了公共方法，代码如下：
    
        import pytest
        
        @pytest.fixture(scope="session")
        def open():
            print("打开浏览器")
            yield
            
            print("执行teardown")
            print("最后关闭浏览器")             

##自动执行fixture

如果每条测试用例都需要添加fixture功能，则需要在每一个用例方法里面传入这个fixture的
名字，这里就可以在装饰器里面添加一个参数autouse="true",它会自动应用到所有的方法中，
只是这里没有办法返回值给测试用例。

    @pytest.fixture(autouse="true")
    def myfixture():
        print("this is my fixture")
        
这样每个测试函数都会自动调用这个前置函数。

##fixture传递参数

测试过程中需要大量的测试数据，如果每条测试数据都编写一条测试用例，用例数量将是非常庞大的。
一般我们在测试过程中会将测试用到的数据以参数的形式传入到测试用例中，并为每条测试数据生成
一个测试结果数据。这时候可以使用fixture的参数化功能，在fixture方法加上装饰器
@pytest.fixture(params=[1,2,3]),就会传入三个数据1、2、3分别将这三个数据传入到用例
当中。这里可以传入的数据是个列表。传入的数据需要使用一个固定的参数名request来接收。

    import pytes
    
    @pytest.fixture(params=[1,2,3])
    def data(request):
        return request.param
        
    def test_not_2(data):
        print(f"测试数据: {data}")
        assert data < 5
           

## 多线程并行与分布式执行

pytest-xdist是pytest分布式执行插件，可以多个CPU或主机执行，这款插件允许用户将测试并发
执行（进程级并发），插件是动态决定测试用例执行顺序的，为了保证各个测试能在各个独立线程里
正确的执行，应该保证测试用例的独立性

安装

    pip install pytest-xdist
    
多个CPU并行执行用例，需要在pytest后面添加-n参数，如果参数为auto，会自动检测系统的CPU
数目。如果参数为数字，则指定运行测试的处理器进程数

    pytest -n auto
    pytest -n [num]
    
    
    
##结合pytest-html生成测试报告

安装

    pip install pytest-html
    
执行方法

    pytest --html=path/to/html/report.html
    
结合pytest-xdist使用

    pytest -v -s -n 3 --html=report.html --self-contained-html
    

    
    
    
##参数化用例
把不同的参数，写到一个集合里，然后程序会自动取值运行用例，直到集合为空便结束。
@pytest.mark.parametrize来参数化。

使用parametrize实现参数化

parametrize()方法详解

def parametrize(self,argnames,argvalues,indirect=False,ids=None,scope=None)

- 主要参数说明

    - argsnames：参数名，是个字符串，如中间用逗号分隔则表示为多个参数名
    - argsvalues：参数值，参数组成的列表，列表中有几个元素，就会生成几条用例
    
- 使用方法
    
    - 使用@pytest.mark.paramtrize()装饰器测试方法
    - parametrize('data', param)中的"data"是自定义的参数名，param是引入的参数列表
    - 将自定义的参数名data作为参数传给测试用例test_func
    - 然后就可以在测试用例内部使用data的参数了

    
    @pytest.mark.parametrize('a, b', [(1, 2), (3, 4)])
    def test_answer1(a, b):
        assert func(a) == b
        
        
##  多次组合使用parametrize

同一个测试用例还可以同事添加多个@pytest.mark.parametrize装饰器，多个parametrize的
所有元素互相组合（类似笛卡尔积),生成大量测试用例

    @pytest.mark.parametrize("x", [1,2])
    @pytest.mark.parametrize("y", [8,10,11])
    def test_foo(x,y):
        print(f"测试数据组合x:{x}, y:{y}")

## @pytest.fixture与@pytest.mark.parametrize结合实现参数化

如果测试数据需要在fixture方法中使用，同时也需要在测试用例中使用，可以在使用parametrize
的时候添加一个参数indirect=True，pytest可以实现将参数传入到fixture方法中，也可以在当
前的测试用例中使用。

    test_user_data = ["Tome", "Jerry"]
    @pytest.fixture(scope="module")
    def login_r(request):
        user = request.param
        print(f"\n 登陆用户:{user}")
        return user
    
    @pytest.mark.parametrize("login_r", test_user_data, indirect=True)
    def test_login(login_r):
        a = login_r
        print(f"测试用例中login的返回值；{a}")
        asset a != ""
 
 
##数据驱动（yaml）

pytest结合YAML

yaml是一个可读性搞，用来表达数据序列化的格式。pyyaml模块在python中用于处理yaml格式数据，
主要使用yaml.safe_dump()和yaml.safe_load()函数将python值和yaml格式数据相互转换。
工作中常常使用YAML格式的文件存储测试数据。

安装

    pip install PyYAML

案例
    
    @pytest.mark.parametrize('a, b', yaml.safe_load(open("./data.yaml")))
    def test_answer2(a, b):
        assert func(a) == b

##结合allure生成测试报告

安装

    下载allure
    
    配置环境变量
    
    查看allure版本：
    
        allure --version 
    
    安装pytest-allure
        
        pip install pytest-allure    
         

运行

- pytest --alluredir=报告生成路径
- 启动allure服务，展示报告
    
    - allure serve 报告路径
    
    - allure generate ./result/ -o 报告路径&& allure open -h 127.0.0.1 -p 8883 报告路径

allure重点页面介绍：

- Behaviors页面， 安装FEATURES和STORIES展示测试用例的执行结果
- Suites页面，Allure测试报告将每一个测试脚本，作为一个Suite。在首页里点击Suites区域
内的任何一条Suite，都会进入Suites页面
- Graphs页面，展示了此次测试结果的统计信息，比如测试用例执行结果状态、测试用例重要等级
分布、测试用例执行时间分布等
- 测试用例详情页面。       
    
    
##前端自动化测试-百度搜索功能实战

    import allure
    import pytest
    import yaml
    from selenium import webdriver
    import time
    # 用例标识，给定用例的链接，可以与用例的管理地址关联
    @allure.testcase("http://www.github.com")
    # 功能模块划分，方便管理和运行测试用例。
    @allure.feature("百度搜索")
    @pytest.mark.parametrize("test_data1", yaml.safe_load(\open("data/data.yml")))
    def test_steps_demo(test_data1):
        # 添加测试步骤
        with allure.step("打开百度网页"):
            driver = webdriver.Chrome()
            driver.get("http://www.baidu.com")
            driver.maximize_window()
    
        with allure.step(f"输入搜索词:{test_data1}")
            driver.find_element_by_id("kw").send_keys(test_data1)
            time.sleep(2)
            driver.find_element_by_id("su").click()
            time.sleep(2)
           
        with allure.step("保存图片")
            driver.save_screenshot("./result/b.png")
            # 链接图片文件
            allure.attach.file("./result/b.png", \
            attachment_type=allure.attachment_type.PNG)
        
        with allure.step("关闭浏览器"):
            driver.quit()
            

执行：

    pytest test_baidudemo.py -s -q --alluredir=./result/
    
    allure serve ./result/
               

