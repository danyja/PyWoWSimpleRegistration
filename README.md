# PyWoWSimpleRegistration
A sample [cmangos](https://github.com/cmangos) WOW registration and management web. 

Referred to [WoWSimpleRegistration](https://github.com/masterking32/WoWSimpleRegistration).

Only tested with the [cllassic](https://github.com/cmangos/mangos-classic) version on Windows. 

# How to use
1. install python, better >3.10.  
安装python，建议大于3.10。请设置pip国内源。

2. clone the code or download as zip then unzip it.  
克隆代码或下载为zip包并解压。

3. run the "install.bat" script to install the venv.  
运行“install.bat”脚本安装虚拟环境。注意中文版有GB2312和utf8两种编码，如果乱码，请换一个试试。

4. edit the "config.py" in instance folder.  
修改instance文件夹下的“config.py”

5. run the "run_wow.bat" and access "http://localhost:5000". Note: If you want to publish to the public network, please use Ngix or Apache reverse proxy.  
运行“run_wow.bat”脚本，浏览器访问“http://localhost:5000”。 注意：如果要发布到公网，请使用Ngix或Apache反向代理。


# Apache + mod-wsgi反代
1. 安装Apache和mod_wsgi (需要编译安装，这里附带一个我安装过的whl包，venv\Scripts\pip install mod_wsgi-5.0.2-cp310-cp310-win_amd64.whl)  
2. 运行 venv\Scripts\mode_wsgi-express module-config，将显示内容添加到Apache配置文件中。  
3. 配置虚拟主机将所有访问定向到main.wsgi  

以下供参考：
```
Listen 5000

LoadFile "C:/Software/Python310/python310.dll"
LoadModule wsgi_module "D:/PyWoWSimpleRegistration/venv/lib/site-packages/mod_wsgi/server/mod_wsgi.cp310-win_amd64.pyd"
WSGIPythonHome "D:/PyWoWSimpleRegistration/venv"

<VirtualHost *:5000>
    WSGIScriptAlias / "D:/PyWoWSimpleRegistration/main.wsgi"
    <Directory "D:/PyWoWSimpleRegistration/">
        Require all granted
    </Directory>
</VirtualHost>
```
