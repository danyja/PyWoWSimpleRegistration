# PyWoWSimpleRegistration
A sample [cmangos](https://github.com/cmangos/issues) WOW registration and management web. 

Referred to [WoWSimpleRegistration](https://github.com/masterking32/WoWSimpleRegistration).

Only tested with the [cllassic](https://github.com/cmangos/mangos-classic) version on Windows. 

# How to use
1. install python, better >3.10.  
安装python，建议大于3.10。请设置pip国内源。

2. clone the code or download as zip then unzip it.  
克隆代码或下载为zip包并解压。

3. run the "install.bat" script to install the venv.  
运行“install.bat”脚本安装虚拟环境。注意中文版（install_chs.bat），编码格式是GB2312。

4. edit the "config.py" in instance folder.  
修改instance文件夹下的“config.py”

5. run the "run_wow.bat" and access "http://localhost:5000". Note: If you want to publish to the public network, please use Ngix or Apache reverse proxy.  
运行“run_wow.bat”脚本，浏览器访问“http://localhost:5000”。注意：如果要发布到公网，请使用Ngix或Apache反向代理。
