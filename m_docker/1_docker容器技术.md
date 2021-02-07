# Docker容器技术

容器技术介绍

Docker是一个开源的应用容器引擎，基于Go语言开发，Docker可以让开发者
打包他们的应用以及依赖包到一个轻量级、可移植的容器中，然后发布到任何
流行的系统。

Docker是世界领先的软件容器平台，Docker官方的口号是“调试你的应用，
而不是调试环境”。在进行多人协作开发时，开发者可以使用Docker来消除
所谓“我这里运行是好的”（works on my machine)问题，运维人员使用
Docker来并行的运行和管理应用来获得更优计算密度，基于各自独立的容器，
不会因为环境原因导致应用运行错误。

所以在Docker横空出世之前，应用打包一直是大部分研发团队的痛点，在
Docker出现后，它以更高效的利用系统资源、更快速的启动时间、一致的
运行环境、持续交付和部署、更轻松的迁移、更轻松的维护和拓展，6大优点
迅速火了起来。

Docker的三个概念：

- 镜像（Image）：是一个包含有文件系统的面向Docker引擎的只读模块。
任何应用程序运行都需要环境，而镜像就是用来提供这种运行环境的。例如
一个Ubuntu镜像就是一个包含Ubuntu操作系统环境的模板。
- 容器（Container）：类似于一个轻量级的沙盒，可以将其看作一个极简
的Linux系统环境（包括root权限、进程控件、用户空间和网络空间等），以及
运行在其中的应用程序。Docker引擎利用容器来运行、隔离各个应用。容器
是镜像创建的应用实例，可以创建、启动、停止、删除容器，各个容器之间是
相互隔离的，互不影响。

注意：镜像本身是只读的，容器从镜像启动时，Docker在镜像的上层创建一个
可写层，镜像本身不变。

- 仓库（Repository）：镜像仓库，是Docker用来集中存放镜像文件的地方。


## Docker安装

Docker是开源的商业产品，有两种版本：社区版（Community Edition，
缩写为CE）和企业版（Enterprise Edition，缩写为EE）。企业版包含
了一些收费服务，一般用不到。我们下面将会演示Docker CE版本的使用方法。

Docker支持很多操作系统平台，有大家常用的Microsoft Windows系列操作
系统（Docker不支持Windows 10家庭版系统），Linux发行版和macOS系统。

### 安装

- Windows上有两种安装Docker方式：
    - 访问Docker网站下载Docker Desktop软件的exe文件
    - 使用Chocolatey包管理工具安装Docker。
      
- Linux发行版Ubuntu系统安装方法

1.切换到管理员权限
    
    su root
    
2.安装必要的一些系统工具

    apt-get update
    
    apt-get -y install apt-transport-https ca-certificates curl\
    software-properties-common
    
3.安装GPG证书

    curl -fsSL \
    http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg \
    | sudo apt-key add -
    
4.写入软件源信息

    add-apt-repository "deb [arch=amd64]\
    http://mirrors.aliyun.com/docker-ce/linux/ubuntu \
    $(lsb_reelease -cs) stable"

5.更新并安装Docker-CE

    apt-get -y update
    apt-get -y install docekr-ce
    
- Linux发行版CentOS系统安装方法

1.切换到管理员权限

    su root
    
2.安装必要的一些系统工具

    yum install -y yum-utils device-mapper-persistent-data lvm2

3.添加软件源信息

    yum-config-manager --add-repo \
    http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

4.更新并安装Docker-CE
    
    yum makecache fast
    yum -y install docker-ce
    
## 常用操作

启动Docker

    systemctl start docker
    
重启

    systemctl retart docker
    
开机时自动启动Docker

    systemctl enable docker

查看Docker运行状态

    systemctl status docker

- macOS上有两种安装Docker方式
                                                     
- 第一种：访问Docker网站下载Docker Desktop的dmg安装包
                                                     
- 第二种：使用包管理工具方式来安装Docker，使用Homebrew工具安装Docker。

    
    brew cask install docker

## Docker 加速器配置

我们下载Docker镜像的时候，默认会访问Docker网站，而Docker网站是在
国外部署的，距离比较远下载速度特别慢。我们可以通过设置加速器的方式来
加速Docker镜像下载的速度。下面将描述一下使用加速器的步骤：

1.使用阿里云提供的Docker镜像加速器服务，https://cr.console.aliyun.com/

2.选择"镜像加速器"

3.根据个人的系统平台，选择运行Docker的OS，并按照操作文档的要求修改
Docker配置文件，然后重启Docker服务即可完成加速器的配置。

### Docker常用命令

Docker的常用命令一般分为：镜像管理、容器管理

查看Docker版本

    docker version

### 镜像管理命令

下面使用busybox软件作为示例，busybox软件是一个集成了非常多最常用的Linux
命令和工具的软件集合。

查看所有镜像

    docker images

- REPOSITORY：镜像来自哪个仓库   
- TAG：镜像的标签信息，版本之类的信息   
- IMAGE ID：镜像创建时的id   
- CREATED：镜像创建的时间   
- SIZE：镜像文件大小

下载软件镜像   
    
    docker pull busybox:latest
- latest表示使用busybox软件的最新版本，所以软件默认下载都是latest版本。

导出镜像

    docker save busybox > busybox.tar
- 把busybox镜像导出为busybox.tar文件，可以把busybox.tar文件复制到别的
操作系统上使用，免除下载时网络慢的问题。    


删除镜像

    docker rmi busybox:latest
    
- 镜像一般都会根据版本打包，如果有下载一个软件的多版本就需要指定具体
版本信息。如busybox:1.26就会删除busybox软件的1.26版本的镜像，不会
删除latest版本的镜像。

导入镜像

    docker load < busybox.tar
    
- 使用导出命令导出的镜像，可以通过此命令导入到没有下载此软件的操作系统，
方便网络条件差的情况使用。

更改镜像名

    docker tag busybox:latest busybox:test

- busybox:latest源镜像名，busybox:test要改成的镜像名

### 容器管理命令

容器运行

    docker run -d --name=busybox:latest ping 114.114.114.114
- run: run参数代表启动容器
- -d: 以后台daemon的方式运行
- --name: 指定一个容器的名字，此后操作都需要使用这个名字来定位容器。
- busybox:latest: 容器所使用的镜像名字
- ping 114.114.114.114: 启动容器执行的命令

查看运行的容器

    docker ps

查看所有容器

    docker ps -a
    
- CONTAINER ID： 容器启动的id        
- IMAGE： 使用哪个镜像启动的容器       
- COMMAND：启动容器的命令       
- CREATED：创建容器的时间       
- STATUS：容器启动时间       
- PORTS：容器映射到宿主机的端口       
- NAMES：容器启动的名字

启动容器

    docker start busybox

重新启动容器

    docker restart busybox

停止容器

    docker stop busybox
    
杀死容器

    docker kill busybox

删除运行中的容器

    docker rm -f busybox

执行容器内命令

    docker exce -it busybox ls
- -it交互终端

复制容器内文件

    docker cp busybox:/etc/hosts hosts
    
查看容器日志

    docker logs -f busybox
    
## 搭建Web服务器nginx

Nginx是一个异步的Web服务器，主要提供Web服务器、反向代理、负载均衡
和HTTP缓存功能。由Igor Sysoev创建于2004年，使用C语言开发。

从Docker hub下载Nginx镜像

    docker pull nginx：1.17.9
    
运行Nginx容器
    
    docker run -d --name nginx -p 8088:80 nginx:1.17.9
- -p:映射容器的端口到宿主机，前面宿主机端口，后面容器端口。

## 挂载目录

当我们可以访问Nginx服务的时候，会发现访问的页面时Nginx默认的欢迎页面，
我们要怎样才能访问自定义的页面呢？我们可以用挂载目录的方式让Nginx服务
展示我们想要的页面。

1.当前位置新建一个html目录，里面放一个新建的html文件，名字为index.html,
内容如下。

    <h1>Hogwarts</h1>

2.启动一个Nginx容器

    docker run -d --name nginx1 -p 8089:80 \
    -v ${PWD}/html:/usr/share/nginx/html \
    nginx:1.17.9
    
- -p 8089:80映射容器的80端口到宿主机8089端口。

- -v ${PWD}/html:/usr/share/nginx/html: -v参数代表挂载一个目录
到容器内，前面的目录${PWD}/html代表宿主机的目录，后面的目录/usr/share/nginx/html
代表容器内的目录。它们中间用分号隔开。其中${PWD}是一个系统变量，代表
当前所在的目录。然后我们在访问宿主机的IP和端口查看一下状态。

## 搭建测试用例平台Testlink

Testlink是基于WEB的测试用例管理系统，主要功能是：测试项目管理、产品
需求管理、测试用例管理、测试计划管理、测试用例的创建、管理和执行，并且
还提供了统计功能。

Testlink服务存储数据依赖数据库服务，所以需要先搭建一个数据库。同时数据库
和Testlink服务之间访问需要网络互相通畅，也需要建立一个容器网络。

可以访问Testlink镜像的介绍网站去查看更多信息。

1.新建容器网络

    docker network create testlink-tier
- network代表网络方面的参数
- create代表新建一个网络名字
- testlink-tier是将要建立的网络名字

2.运行MariaDB数据库

    docker run -d --name mariadb \
    -e MARIADB_ROOT_PASSWORD=mariadb \
    -e MARIADB_USER=bn_testlink \
    -e MARIADB_PASSWORD=bn_testlink \
    -e MARIADB_DATABASE=bitnami_testlink \
    --net testlink-tier \
    --volume ${HOME}/docker/mariadb:/bitnami \
    bitnami/mariadb:10.3.22
    
- -e 参数指定
- --net testlink-tier: 指定要使用的网络名字

3.运行Testlink容器

    docker run -d -p 8080:8080 -p 8443:8443 --name testlink \
    -e TESTLINK_DATABASE_USER=bn_testlink \    
    -e TESTLINK_DATABASE_PASSWORD=bn_testlink \    
    -e TESTLINK_DATABASE_NAME=bitnami_testlink \
    --net testlink-tier \ 
    --volume ${HOME}/docker/testlink:/bitnami \
    bitnami/testlink:1.9.20
    
4.浏览器内访问：http://你的IP地址:8080

- 默认用户:user, 默认密码：bitnami 


## 搭建持续集成平台Jenkins

下载Jenkins

    docker pull jenkins/jenkins

启动Jenkins容器

    docker run -d --name=myjenkins -p 8080:8080 jenkins/jenkins
    
通过此种方式启动的Jenkins容器，数据会在Jenkins容器被删除后消失。
如果需要保持Jenins的数据，请查看下面的方式启动Jenkins容器。

Jenkins数据持久化

1.新建Jenins目录并修改权限 新建目录

    mkdir jenkins

更改权限

    chmod 777 jenkins

- 777代表所有用户和组可读写执行

2.启动Jenkins，增加-v参数挂载目录

    docker run --name jenkins -d -p 8080:8080
    -p 50000:50000 -v ${PWD}/jenkins:/var/jenkins_home
    jenkins/jenkins
    
- -p 8080:8080: 8080端口为Jenkins服务的web 访问端口；-p
50000:50000 端口为jenkins和其他jenkins节点通讯用的端口 
             
- -v ${PWD}/jenkisn:/var/jenkins_home: 挂载宿主机${PWD}/jenkins
目录到容器内/var/jenkins_home目录，其中${PWD}

3. 浏览器内访问：http://你的IP地址：8080，进入Jenkins配置页面

4. 使用
    
        docker exec -it jenkins cat             
        /var/jenkisn_home/secrets/initialAdminPassword
        
    获取默认密码。

5. 输入上一步得到的密码，就进入Jenkins服务啦。

## docker-compose使用

docker-compose是用于定义和运行多容器的Docker应用程序的工具。
通过Compose，可以使用YAML文件来配置应用程序的服务。然后，使用一个
命令，就可以从配置中创建并启动所有服务。

Compose可在所有环境中工作：生产，中台，开发，测试以及CI工作流

Compose的使用一般分为三步：

1.使用Dockerfile定义应用程序的环境，以便可以在任何地方复制它。

2.在docker-compose.yml中定义组成应用程序的服务，以便它们可以
在隔离的环境中一起运行。

3.运行docker-compose up，然后Compose启动并运行你的整个应用程序。

### 环境安装

docker-compose的安装

可以访问官方的网站：https://docs.docker.com/compose/install/
查看更多信息。根据个人的系统平台，选择运行docker-compose的版本，
即可完成docker-compose的安装。

Microsoft Windows和macOS的桌面版默认有安装

Linux用户

    curl -L "https://github.com/docker/compose/releases/ \
    download/1.25.4/docker-compose-$(uname -s)-$(uname -m)"\
     -o /usr/local/bin/docker-compose

- 1.25.4是docker-compose的软件版本号，可以访问

    http://github.com/docker/compose/releases/
    
查看更多版本信息。

添加可执行权限

    chmod +x /usr/local/bin/docker-compose
    
最后可以查看docker-compose的版本信息，来确认是否安装成功

    docker-compose version
    
### docker-compose使用

##### 创建文件

1. 创建一个项目目录并进入目录

    mkdir flask_dc && cd flask_dc
    
2. 创建一个app.py文件，并添加下面的内容


    import time
    import redis
    from flask import Flask
    
    app = Flask(__name__)
    cache = redis.Redis(host="redis", port=6379)
    
    def get_hit_count():
        retries = 5
        while True:
            try:
                return cache.incr('hits')
            except redis.exceptions.ConnectionError as exc:
                if retries == 0:
                    raise exc
                retries -= 1
                time.sleep(0.5)

    @app.route('/')
    def hello():
        count = get_hit_count()
        return "Hello World! I have been seen {} times.\n".format(count)                

redis服务需要自己安装配置

3. 创建一个requirements.txt文件，并添加下面的内容，requirements.txt
记录的是python需要的三方库。

    flask
    redis

4. 创建Dockerfile文件，并添加下面的内容


    # 依赖Python3.7镜像，开始构建
    FROM python:3.7-alpine
    # 工作路径设定为/code
    WORKDIR /code
    # 创建环境变量给Flask使用
    ENV FLASK_APP app.py
    ENV FLASK_RUN_HOST 0.0.0.0
    # 安装gcc工具
    RUN apk add --no-cache gcc musl-dev linux-headers
    # 复制requirements.txt到容器内
    COPY requirements.txt requirements.txt
    # 安装python的依赖
    RUN pip install -r requirement.txt
    # 复制项目当前路径给镜像内的工作路径
    COPY . .
    # 为容器设置默认启动命令
    CMD ["flask", "run"]
    
5. 创建一个docker-compose.yml文件，并添加下面的内容。
此yml文件会创建两个容器，web容器和redis容器。version指定
要使用Docker-compose API的版本。services字段定义要使用
的服务，如下面使用的web服务和redis服务。


    version: '3'
    services:
      web:
        bulid:    
        ports:
          - "5000:5000"
      redis:
        image: "redis:alpine"

- web和redis是两个容器服务         
- image指定的是容器启动的镜像名字       
- build是通过Dockerfile的方式构建镜像 

### 运行docker-compose

    运行docker-compose up来启动应用。
    
在浏览器输入http://your ip：5000，即可看到程序运行。刷新一次页面，
统计数字就自动加1.          

## docker-compose常用命令

查看帮助

    docker-compose --help
    
启动命令

    # 启动命令
    docker-compose up
    # 启动后，后台运行服务容器
    docker-compose up -d
    # 启动容器前构建镜像
    docker-compose up -bulid
    
查看当前运行的docker-compose

    docker-compose ps
    
停止容器

    docker-compose stop

启动容器

    docker-compose start

删除容器的数据卷

    docker-compose down --volumes


## Docker的registry介绍

Docker registry是存储Docker image的仓库，运行Docker push、Docker pull、
Docker search时，实际上是通过Docker daemon与docker registry通信。
有时候使用Docker Hub这样的公共仓库可能不方便，我们可以通过registry创建
一个本地仓库。

[浏览器访问registry信息](https://hub.docker.com/_/registry)

下载镜像

    docker pull registry：2.7.1
    
运行

    docker run -d \ 
    -p 5000:5000 \
    -v ${PWD}/registry:/var/lib/registry \
    --restart always \
    --name registry \ 
    registry:2.7.1
    
- --restart always: Docker启动后自动运行这个容器
        
- -v ./registry:/var/lib/registry: 挂载目录

## Docker客户端配置

/etc/docker/daemon.json

    "insecure-registries": [
    "运行registry的服务器IP:5000"
    ]

通过docker push上传镜像
1. 先下载一个镜像，也可以通过Dockerfile构建镜像。


    docker pull ubuntu:18.04

2. 更改镜像信息


    docker tag ubuntu:18.04 192.168.31.60:5000/ubuntu:18.04

- 此IP为registry服务器所有192.168.31.60，可以按照实际服务器IP填写，
可以用IP也可以用域名的方式。

3.推送到本地registry


    docker push 192.168.31.60:5000/ubuntu:18.04

可以访问http://运行registry的服务器IP:5000/v2/_catalog查看registry
容器内推送的镜像信息。

4. 下载registry服务器上的镜像

    
    docker pull 192.168.31.60:5000/ubuntu:18.04
    
- 下载镜像的时候要指定从哪个registry服务器下载。例如192.168.31.60:5000

通过以上操作就可以保存镜像到本地的registry，可以在别的电脑上配置daemon.json
内的信息，然后就可以通过这个registry下载镜像。Docker官方registry服务器功能
有限，它默认是不可以删除镜像的。打击可以了解一下[Harbor](https://github.com/goharbor/harbor)

## Dockerfile语法与指令

        
                
        

                    
        
                   

                                        
            
    
       

                                                       
                                                                             