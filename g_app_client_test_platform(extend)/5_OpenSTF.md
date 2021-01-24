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

