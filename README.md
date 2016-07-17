# megamenu
LSI RAID卡管理小工具megamenu

作者:Patrick Zheng

简介：

本工具旨在简化MegaCli/StorCli/OEM LSI RAID卡的CLI工具的操作，使得命令行工具菜单化，让日常的测试、运维工具更轻松。

本工具仅能在Linux下使用，需要安装MegaCli/StorCli，需要Python2.6或以上版本支持，但是Python3.x版本可能导致未知错误发生，需要Python Snack库支持，Snack库一般情况下都已安装，测试环境：CentOS 6.X，Ubuntu 12.04。

测试用卡：LSI 9271-8i、DELL PERC H830

测试MegaCli版本：8.07.14

测试StorCli版本: 1.15.12

测试PERCCli（DELL LSI OEM卡命令行工具）版本：1.11.03

已知问题：
当有多块不同型号（是否一定是不同型号待确认，也可能是因为和DELL
OEM的卡混插导致的）的RAID卡时，使用StorCli代替MegaCli时会出现部分命令无法取得RAID卡信息的情况，这种情况请尽量使用MegaCli。

可能发生的问题：
远程模块我没有测试过对端如果完全没有安装过MegaCli或是StorCli能不能单靠一个运行文件就run起来，虽然我有试过移除这两种工具的安装，但是也许依赖库没有被移除呢？欢迎大家测试后mail我：zzcahj@163.com

----------------------------------------------
v0.92-remote beta

发布时间：2016.7.17

1、改善远程管理程序配置时出错后的友好程度；
2、增加修改磁盘组缓存设置的功能；
3、BUG修正；
4、文字优化。


----------------------------------------------
v0.91-remote beta

发布时间：2016.7.11

1、增加管理远程主机LSI RAID卡的能力，使用./megamenu-remote.py进入，输入本机地址也可以管理本机啦。

说明：
默认将程序运行目录下的storcli64传输到远端的/tmp目录下，可以根据需要将MegaCli/perccli等工具改名为storcli64（比如storcli64运行出错时），当然也可以直接修改Python脚本:D。
远程能力需要Python的paramiko模块支持，我把pip放在解压后的根目录下了，先安装pip，然后进入paramiko目录pip install * 。
如果有外网的情况下，也可以pip install paramiko或是直接下载paramiko安装包安装。
建议使用pip安装，相对简单些。

--------------------------------
v0.91 beta 

发布时间：2016.7.10

1、增加一个查看和设置磁盘组为BOOT Drive的小功能，便于在Live CD下使用。

--------------------------------
v0.9 beta 

发布时间：2016.7.10

1、增加将物理磁盘添加为全局热备盘或指定为某个DG的热备盘的功能；

2、增加查询指定DG热备盘的功能；

2、界面进一步优化统一，所有的界面都可以通过TAB选择到返回/退出来退出当前选项或程序了；

3、增加了Storcli的运行程序（版本1.15.12，似乎Debian和Redhat系直接都可以使用）；

4、BUG修复。

已知问题：

当有多块不同型号（是否一定时不同型号待确认，也可能是因为和DELL
OEM的卡混插导致的）的RAID卡时，使用StorCli代替MegaCli时会出现部分命令无法取得RAID卡信息的情况，这种情况请尽量使用MegaCli。

--------------------------------
v0.7 beta

更新内容：

1、增加查看状态信息菜单下，磁盘组初始化信息查询选项；

2、增加查看状态信息菜单中物理磁盘信息时，可以选择查看详细信息或磁盘重建进度；

3、若干Bug修正，和CentOS的贴合度更高了；

4、在压缩包内增加了DEB格式的MegaCli安装包，DEB和RPM的MegaCli版本均为8.07.14

--------------------------------
v0.6 beta

更新内容：

1、缓存刷新功能已经可以使用了；

2、界面优化。

（该工具仅能在Linux下使用，需要安装MegaCLI，需要Python2.6或以上版本支持，Python3.x版本可能导致未知错误发生，需要Python Snack库支持，Snack库一般情况下都已安装，测试环境：CentOS6.X，Ubuntu12.04，测试用卡：LSI 9271-8i）

--------------------------------
v0.5 beta

更新内容：

1、压缩为.tar.gz包，包内包含megagui.py主程序及MegaCLI安装包(RPM格式)；

2、在各个菜单上增加了返回按钮，以防在某些版本的Linux下无法用ESC返回;

3、去掉了之前忘记去掉的调试信息；

4、修正了若干个变量调用错误的BUG；

5、重新调整了屏幕刷新函数，防止某些情况下屏幕刷新太多次导致图形不正常的情况.

--------------------------------
v0.2 beta

更新内容：

1、更新了组合DG的添加，可以创建r-10,r-50,r-60磁盘组；

2、增加了外来（Foreign）磁盘信息的检测，可以在状态信息的物理磁盘状态看到是否是外来磁盘（外来磁盘会在磁盘前增加F|标记）；

3、添加DG时会对外来磁盘进行过滤；

4、优化了创建DG时磁盘大小和磁盘数量的检测；

5、添加了-s参数，-s可以手工指定MegaCLI的位置，不使用-s参数则调用/etc/megacliuipath.cfg内的路径，默认是/opt/MegaRAID/MegaCli/MegaCli64，使用过一次-s指定后，/etc/megacliuipath.cfg内的路径也会随之修改；

6、添加了-h参数，可以调用使用帮助；

7、启动增加了MegaCLI命令工作状态的检测，如工作异常则无法启动该工具。

--------------------------------
v0.1 beta

这是megagui.py的第一个版本。

1、可以创建RAID0,1,5磁盘组；

2、可以删除磁盘组；

3、具备RAID卡、物理磁盘、磁盘组信息查询功能；

4、可以快速开关JBOD模式；

5、可以快速将剩余(unconfig good)磁盘制作成单盘RAID0；

6、可以定位磁盘在盘柜上的位置(磁盘灯闪烁)。
