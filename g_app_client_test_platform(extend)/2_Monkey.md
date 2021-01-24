# Monkey

Monkey是一个在模拟器或设备上运行的程序，它生成用户事件
的伪随机流，例如单击、触摸或手势，以及许多系统级事件。
也可以使用Monkey以随机但可重复的方式对正在开发的应用
程序进行压力测试。

Monkey属于自动化遍历工具，我无需编写代码就可以实现移动
端页面点击，输入等常见操作，当页面中存在大量元素时，可借用
Monkey工具替代手工点击。

环境安装

Android SDK提供了Android API库和开发工具构建，测试和
调试应用程序。其中就包括Monkey工具，配置Android SDK的
环境变量后就可以在命令行使用。

使用

Monkey是一个命令行工具，可以在任何模拟器实例或设备上运行。
它将用户事件的伪随机流发送到系统中：其功能主要分为四类：

- 基本配置选项，例如设置事件数量
- 操作约束，例如对指定App进行测试
- 事件类型和频率
- 调试选项

可以通过adb shell monkey命令启动Monkey
    
    adb shell monkey [option] <事件计数>
    
在没有指定选项的情况下，Monkey将以安静模式启动，并将
事件发送到设备上的所有包。>参数做标题感觉很突兀，建议修改
为-p或者参数-p，加一些文字性说明，阅读的感觉会更好。

#### p:指定应用
    
指定一个或多个应用，指定应用之后，monkey将只允许系统启动指定的app

一个应用：

    adb shell monkey -p com.xueqiu.android 100
    
多个应用

    adb shell monkey -p com.ifext.news -p com.xuqiu.android 100
    
#### s:随机数

伪随机数生成器的seed值。当我们希望多次测试的随机值相同
时，需要设置相同的seed值，它将生成相同的事件序列：

测试1：

    adb sell monkey -p com.xueqiu.android -s 20 80

测试2：
    
    adb shell monkey -p com.xueqiu.android -s 20 80

#### v:日志   

显示monkey日志，包括-v，-vv，-vvv三个级别-v提供启动信息
，少量结果信息。-vv提供详细的日志信息（activity）-vvv
提供详细的日志信息（所有activity）

#### throttle:事件延迟

用户指定用户操作（即事件）间的延时，单位是毫秒

    adb shell monkey -p com.xueqiu.android --throttle 5000 100
    
#### ignore-crashes:崩溃继续

应用程序崩溃后，Monkey依然会发送事件，直到事件计数完成

    adb shell monkey -p com.xueqiu.android --ignore-crashes 1000

#### kill-process-after-error: 错误停止

当应用程序发生错误时，应用程序停止运行并保持在当前状态
（注意：应用程序仅是静止在发生错误时的状态，系统并不会
结束该应用程序的进程）

    adb shell monkey -p com.xueqiu.android --kill-process-after-error 1000

### pct 事件百分比

Monkey由多个事件组成，测试过程中会偏重一些事件，比如需要
更多的触摸事件，更少的导航动作。 

--pct-touch调整触摸事件的百分比，触摸事件是一个down-up事件，
即在屏幕某处按下并抬起的操作，比如一个应用90%的操作都是触摸，
那就可以将此参数的百分比设置成相应较高的百分比

    adb shell monkey -p com.xueqiu.android --pct-touch 10 1000                

--pct-motion: 调整动作事件的百分比，动作事件由屏幕上某处的
一个down事件、一系列的伪随机事件和一个up事件组成，比如直线滑动
（不包含曲线滑动）：

    adb shell monkey -p com.xueqiu.android --pct-motion 20 1000
    
--pct-trackball：调整轨迹事件的百分比，轨迹事件由一个或几个
随机的移动组成，有时还伴随点击，包含曲线滑动：

    adb shell monkey -p com.xueqiu.android --pct-trackball 30 1000

--pct-majornav:调整“主要”导航事件的百分比，比如回退按键、彩蛋按钮：

    adb shell monkey -p com.xueqiu.android --pct-majornav 50 1000
    

#### 案例

在雪球页面生成200个随机事件

- 安装雪球app            
- 打开雪球app           
- 在目录行输入monkey命令：


    # 生成200个随机事件，并打印详细日志内容
    adb shell monkey -p com.xueqiu.android -vv 200
    
    # 生成200个随机事件，触摸占比50%，动作占比20%，导航占比30%，每个事件间存在1s延迟。
    adb shell monkey -p com.xueqiu.android --pct-touch 50\
    --pct-motion 20 --pct-nav 30 -vv --throttle 1000 200
               
                
        