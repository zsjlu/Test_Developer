# OpenSTF

OpenSTF是一个手机设备管理平台，可以对手机进行远程管理、
调试、远程手机桌面监控等操作。它使用nodejs和angularjs开发，
遵循apache license2.0开源协议。

移动端测试需要不同型号的设备，如果为每个测试人员都分配移动设备，
则需要成本开销，OpenSTF可以实现人机分离，远程对设备进行控制，
解决了多设备共用的问题。

[github地址](https://github.com/openstf/stf)

主要有以下几个功能

- 在Web上管理多个android设备
- 支持Android多个版本（2.3.3~8.0），而且不需要root
- 实时屏幕操作和显示
- 支持adb connect远程连接调试
- 可以从PC机键盘输入到远程的android设备中
- 安装卸载APK
- android设备信息的展示（网络装填、MIME、android版本、手机型号）
- 远程开关机、远程开关WIFI、截屏、LogCat等等。

环境安装

macos安装可参考官网，下面介绍docker安装

1.拉取STF相关镜像

    # 拉取STF镜像
    docker pull openstf/stf:latest
    # 拉取adb镜像
    docker pull sorccu/adb:latest
    # 拉取rethinkdb 镜像
    docker pull rethinkdb:latest
    
2.查看拉取下来的镜像

    docker images

3.启动镜像

启动数据库rethinkdb
    
    docker run -d --restart=always --name rethinkdb -v /srv/rethinkdb:/data --net host rethinkdb rethinkdb --bind all --cache-size 500 --http-port 8090
    
启动adb service

    docker run -d --restart=always --name adbd --privileged -v /dev/bus/usb:/dev/bus/usb --net host sorccu/adb:latest
    
启动stf

    # 本机
    docker run -d --restart=always --name stf --net host openstf/stf
    stf local --allow-remote
    
    # 非本机
    docker run -d --restart=always --name stf --privileged=true --net host openstf/stf stf local --public-ip 192.168.0.105 --adb-host 192.168.0.107 --adb-port 5037 --allow-remote

    
4.登陆STF在浏览器地址栏输入http://localhost:7100即可进入登陆界面，
输入用户名和密码后即可进入


#### 使用 

连接移动设备后就可以在stf页面进行操作，操作过程完全模拟手机，
没有任何难度，也可以在功能区实现快捷操作。                     

获取手机ip，并允许usb调试

在电脑命令行输入

    adb tcpip 5555
    
    adb connect ip:5555
    
当出现connected时说明连接成功

### 问题：我已经连接上了容器中的adb，但是没有再stf中查看到设备    