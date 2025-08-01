@echo off
setlocal enabledelayedexpansion

:: 设置颜色
color 0A
title Python环境配置工具

:: 强制切换到脚本所在目录
set "script_dir=%~dp0"
cd /d "%script_dir%"
echo 当前工作目录: %cd%

:: 检查Python安装
echo 正在检测Python安装...
for /f "tokens=*" %%a in ('where python 2^>nul') do (
    set "python_path=%%a"
)

if not defined python_path (
    echo.
    echo 错误: 未检测到Python安装。
    echo 请从 https://www.python.org/downloads/ 下载并安装Python
    echo 并确保在安装时勾选"Add Python to PATH"选项
    echo.
    pause
    exit /b 1
)

:: 获取Python版本
for /f "tokens=*" %%v in ('"%python_path%" --version 2^>^&1') do (
    set "python_version=%%v"
)

:: 检查Python版本是否≥ 3.10
echo 检测到安装的Python版本: %python_version%
python -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" && (
    echo Python版本满足 ≥ 3.10
) || (
    echo 错误: 需要Python ≥ 3.10
    pause
    exit /b 1
)

:: 检查pip是否可用
echo 正在检查pip是否可用...
"%python_path%" -m pip --version > nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo 错误: pip不可用
    echo 请确保Python安装正确或尝试运行: "%python_path%" -m ensurepip --upgrade
    echo.
    pause
    exit /b 1
)

:: 检查虚拟环境模块
echo 正在检查venv模块...
"%python_path%" -c "import venv" 2>&1
if %errorlevel% neq 0 (
    echo.
    echo 错误: venv模块不可用
    echo 尝试修复: "%python_path%" -m ensurepip --upgrade
    echo 或重新安装Python并确保勾选所有可选组件
    echo.
    pause
    exit /b 1
)

:: 创建虚拟环境
set "venv_dir=venv"
if exist "%venv_dir%" (
    echo [WARN] 虚拟环境目录已存在
    choice /c YN /m "是否重新创建虚拟环境?"
    if /i !errorlevel! == 1 (
        echo 正在删除旧虚拟环境...
        rmdir /s /q "%venv_dir%"
        if exist "%venv_dir%" (
            echo.
            echo 错误: 无法删除虚拟环境目录
            echo 请手动删除 %venv_dir% 文件夹后重试
            echo.
            pause
            exit /b 1
        ) else (
            echo 删除成功
        )
    ) else (
        echo 使用现有虚拟环境
        goto activate_venv
    )
) else (
    echo 虚拟环境目录不存在，将创建新环境
)

echo 正在创建虚拟环境...
"%python_path%" -m venv "%venv_dir%"
if %errorlevel% neq 0 (
    echo.
    echo 错误: 创建虚拟环境失败
    echo 可能原因:
    echo 1. 权限不足 - 尝试以管理员身份运行此脚本
    echo 2. 防病毒软件阻止 - 暂时禁用防病毒软件
    echo 3. Python安装损坏 - 尝试修复Python安装
    echo.
    pause
    exit /b 1
)

:activate_venv
:: 激活虚拟环境并安装依赖
echo 正在激活虚拟环境...
call "%venv_dir%\Scripts\activate.bat"
if %errorlevel% neq 0 (
    echo.
    echo 错误: 无法激活虚拟环境
    echo 请检查 %venv_dir%\Scripts\activate.bat 是否存在
    echo.
    pause
    exit /b 1
)

:: 检查requirements.txt是否存在
if not exist "requirements.txt" (
    echo.
    echo 警告: 未找到requirements.txt文件
    echo 将跳过依赖安装步骤
    echo.
    goto success
)

echo 正在安装requirements.txt中的依赖...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo 错误: 依赖安装失败
    echo 尝试运行: %venv_dir%\Scripts\python.exe -m pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

:success
echo.
echo 环境配置完成!
echo Python路径: %python_path%
echo Python版本: %python_version%
echo 虚拟环境已创建在: %cd%\%venv_dir%
echo 当前工作目录: %cd%

pause