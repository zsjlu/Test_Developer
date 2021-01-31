## apiobject模式与原则

在普通的接口自动化测试中，如果接口的参数，比如url，headers等传参改变，
或者测试用例的逻辑、断言改变，那么整个测试代码都需要改变。apiobject
设计模式借鉴了pageobject的设计模式，可以实现一个优雅、强大的配置文件。


理念

apiobject设计模式可以简单分为6个模块，分别是API对象、接口测试框架、
配置模块、数据封装、Utils、测试用例。

- 接口测试框架：base_api，完成对api的驱动
- API对象：继承base_api后，完成对接口的封装
- 配置模块：完成配置文件的读取
- 数据封装：数据构造与测试用例的数据封装
- Utils：其他功能封装，改进原生框架不足
- 测试用例：调用Page/API对象实现业务并断言

枯燥的讲述概念可能难以理解，后面的章节都会围绕这些模块进行理论的拆解
和实例的演示。

### apiobject模式应用

    import requests
    
    class TestDemo:
    
        def test_get_token(self):
            r = requests.get(url="https://qyapi.weixin.qq.com/cgi-bin/gettoken",
                params = {"corpid":"ww93348658d7c66ef4", 
                      "corpsecret":"..."}
                      )
            return r.json()['access_token']
            
        def test_department_list(self):
            r = requests.get(url="https://qyapi.weixin.qq.com/cgi-bin/department/llist",
                            params={"access_token": self.test_get_token(),
                            "id":1})
            assert r.json()["errcode"] == 0
            return print(r.json())
            
思路

    |-__init__.py
    |-api
    |  |-__init__.py
    |  |-base_api.py
    |  |-department.py
    |  |-wework.py
    |-data
    |  |-department_list.yml
    |-testcases
    |  |-__init__.py
    |  |-test_department_list.py
    |-utils
       |-__init__.py
       |-utils.py
       

- api
    - base_api.py是用来封装所有api的通用方法，比如打印log、对断言工具
    做二次封装等，不牵涉与业务相关的操作                                   
    - wework.py继承base_api并实现基本业务，之后所有的具体的业务资源继承
    自wework，比如token的获取等；                                   
    - department继承自wework，用来实现对应模块具体的业务逻辑，比如发送
    请求，请求内有什么参数等等。                                    
- testcases文件夹内统一存放所有的测试用例，调用API对象实现业务并断言                                   
- utils文件夹内存放对其他功能封装，改进原生框架不足                                   
- data文件夹数据构造与测试用例的数据封装，此外，还有配置模块与数据封装
会在后面的章节进行具体的介绍

实战

utils.py在此文件中封装一个jsonpath方法。
    
    import json
    from jsonpath import jsonpath
    
    class Uitls:
        @classmethod
        def jsonpath(cls, json_object, expr):
            return jsonpath(json_object, expr)

base_api.py，在此文件中调用utils中的jsonpath方法。

    from test_wework.utils.Utils import Utils
    
    class BaseApi:
        json_data = None
        
        def jsonpath(self, expr):
            return Utils.jsonpath(self.json_data, expr)

wework.py，继承类BaseApi，实现token的获取。将在后面"通用api封装"
章节中详细讲述函数内部的设计。

    class WeWork(BaseApi):
        corpid = "..."
        contact_secret = "..."
        token = dict()
        token_url = ".."
        
        @classmethod
        def get_token(cls, secret=contact_secret):
            if secret not in cls.token.keys():
                r = cls.get_access_token(secret)
                cls.token[secret] = r["access_token"]
            return cls.token[secreet]
        
        @classmethod
        def get_access_token(cls, secret):
            r = requests.get(cls.token_url,
                            params={"corpid": cls.corpid,
                                    "corpsecret": secret})
            return r.json()
            
department.py，继承类WeWork，发起一个get请求，获取department的list。

    class Department(BaseApi):
        list_url = "..."
        
        def list(self, id):
            self.json_data = requests.get(self.list_url, 
                            params={"access_token":WeWork.get_contact_token(),
                                    "id":id}).json()
            return self.json_data

test_department.py，断言返回值中的第一个name是否为"WestWayyt"

    class TestDepartment:
        department = Department()
        
        def test_department_list(self):
            r = self.department.list(1)
            assert self.department.jsonpath(expr="$..name")[0] == "WestWayyt"

## 通用api封装

在apiobject设计模式中，需要一个“base_api”作为其他api步骤的父类，把
通用功能放在这个父类中，供其他的api直接继承调用。这样做的优点在于，减少
重复代码，提高代码的复用性。

实战练习

上一章节在演示使用api-object设计模式对脚本进行改造时提到了base_api。
不过在上一章，仅仅只是封装了一个utils中的一个简单方法。并没有完全
体现出base_api的实际作用。接下来会通过通用接口协议的定义与封装实战，
实际体会一下base_api的巧妙之处。

base_api.py，在代码内，对requests进行一层封装，当然在这里还看不出
来具体的优势：

    import requests
    
    class BaseApi:
    
        def request(self, method, url, **kwargs):
            self.json_data = requests.request(method=method, url=url, **kwargs)
            return self.json_data
            
wework.py，继承于类BaseApi，可以直接调用父类中的request方法（不需要
导入requests库），从而发起一个get请求：

    from test_interface.test_wework.api.base_api import BaseApi
    
    class WeWork(BaseApi):
        corpid = "..."
        contact_secret = "..."
        token = dict()
        token_url = "..."
        
        def get_access_token(self):
            r = self.request(method="get", url=self.token_url,
                            params={"corpid": self.corpid,
                                    "corpsecret": self.contact_secret})
            return r.json()


test_wework.py，继承于类WeWork，主要目的只是为了检查上面的get_access_token(self)是否
成功：

    from test_interface.test_wework.api.wework import WeWork
    
    class TestWeWork(WeWork):
        
        def test_get_access_token(self):
            r = self.get_accesss_token()
            assert r["errcode"] == 0
            
在上面的案例中，在base_api.py中对requests进行了多一层的封装，这样子，
只要是属于BaseApi这个类的子类，都可以无需引用而直接调用requests库。
从而发起各种各样的请求，实现了通用接口协议的定义与封装。

## 测试步骤的数据驱动

理念与同“UI 自动化测试框架”中的“测试步骤的数据驱动”相同，接口中的测试步骤
的数据驱动就是将接口的参数封装到yaml文件中管理。当测试步骤发生改变，
只需要修改yaml文件中的配置即可。

测试数据的数据驱动

数据驱动就是数据的改变从而驱动自动化测试的执行，最终引起测试结果的改变。
简单来说，就是参数化的应用。数据量小的测试用例可以使用代码的参数化来
实现数据驱动，数据量大的情况下建议使用一种结构化的文件来对数据进行存储，
然后在测试用例中读取这些数据。

#### 参数化实现数据驱动

原理与前面章节“UI 自动化测试框架”中的“测试数据的数据驱动”大同小异。依然
使用@pytest.mark.parametrize装饰器来进行参数化，使用参数化来实现
数据驱动。

    import pytest
    
    class TestDepartment:
        department = Department()
        
        @pytest.mark.parametrize("id",[2, 3])
        def test_department_list(self, id):
            r = self.department.list(id)
            assert self.department.jsonpath(expr="$..parentid")[0] == 1

上面的代码首先使用@pytest.mark.parametrize装饰器，传递了两组数据，
测试结果显示有两条测试用例被执行，而不是一条用例。也就是pytest会将两组
测试数据自动生成两个对应的测试用例并执行，生成两条测试结果。

#### 使用yaml文件实现数据驱动

当测试数据量大的情况下，可以考虑把数据存储在结构化的文件中。从文件中
读取出代码中所需要格式的数据，传递到测试用例中执行。本次实战以YAML进行
演示。YAML以使用动态字段进行结构化，它以数据为中心，比其他数据格式更
适合做数据驱动

    class TestDepartment:
    
        department = Department()
        
        @pytest.mark.parametrize("id",\
        yaml.safe_load(open("../data/department_list.yml")))
        def test_department_list(self, id):
            r = self.department.list(id)
            assert self.department.jsonpath(expr="$..parentid")[0] == 1
            
## 配置的数据驱动

实际工作中，对于缓解的切换和配置，为了便于维护，通常不会使用硬编码的形式
完成。在“多环境下的接口测试”章节中已经介绍了，如何将环境的切换作为一个
可配置的选项。

    # 把host修改为ip，并附加host header
    env = {
    "docker.testing-studio.com": {
        "dev": "127.0.0.1",
        "test": "1.1.1.2"
        },
        "default":"dev"
        }
        
        data["url"]=str(data["url"]).replace(
            "docker.testing-studio.com",
            env["docker.testing-studio.com"][env["default"]]
            )
            
        data["headers"]["Host"]="docker.testing-studio.com"
### 实战
        
依然以yaml为示例，将所有的环境配置信息放到env.yml文件中。如果怕出错，
可以先使用yaml.safe_dump(env)将dict格式的代码转换为yaml。                                                                                                        