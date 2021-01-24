# Maxim

[Maxim](https://github.com/zhangzhao4444/Maxim)
是居于Monkey二次开发的工具，可以对页面实现高速点击。

环境安装

- 支持Android5, 6, 7, 8, 真机及模拟器；Android 5不支持dfs mode

- 将framework.jar, monkey.jar push到手机上某个目录中，建议/sdcard

    
    adb push framework.jar /sdcard
    adb push monkey.jar /sdcard
    
用法

下载AppetizerIO:APP测试->UI压力测试，支持多种模式，黑名单，
所有配置文件（自动json语法查错），测试开始前自动push
配置文件

测试过程log实时更新

一键错误log上报作者

#### 命令行模式

cmd命令：

    adb shell CLASSPATH=/sdcard/monkey.jar:/sdcard/framework.jar\
    exec app_process /system/bin/ tv.panda.test.monkey.Monkey\
    -p com.panda.videoliveplatform --uiautomatormix \
    --running-minutes 60 -v -v
    

- tv.panda.test.monkey.Monkey: monkey入口类，不要修改        
- com.panda.videoliveplatform: 被测app包名，需要修改       
- --uiautomatormix: 遍历策略

策略

1.模式DFS-uiautomatordfs增加深度遍历算法       

2.模式Mix-uiautomatormix直接使用底层accessibiltyserver
获取界面接口解析各控件，随机选取一个空间执行touch操作。
同时与原monkey其他操作按比例混合使用。默认accessibilityserver
action占比50%，其余各action分剩余的50%accessibilityserver
action 占比可配置 --pct-uiautomatormix n  

3.模式Troy-uiautomatortroy控件选择策略按max.xpath.selector
配置的高低优先级来进行深度遍历

4.保留原始monkey

5.总运行时长 -running-minutes 3运行3分钟

6.-act-whitelist-file /sdcard/awl.strings定义白名单 -act-blacklist-file

其他参数与原始monkey一致。

      