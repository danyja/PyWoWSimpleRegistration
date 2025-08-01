@echo off
setlocal enabledelayedexpansion

:: ������ɫ
color 0A
title Python�������ù���

:: ǿ���л����ű�����Ŀ¼
set "script_dir=%~dp0"
cd /d "%script_dir%"
echo ��ǰ����Ŀ¼: %cd%

:: ���Python��װ
echo ���ڼ��Python��װ...
for /f "tokens=*" %%a in ('where python 2^>nul') do (
    set "python_path=%%a"
)

if not defined python_path (
    echo.
    echo ����: δ��⵽Python��װ��
    echo ��� https://www.python.org/downloads/ ���ز���װPython
    echo ��ȷ���ڰ�װʱ��ѡ"Add Python to PATH"ѡ��
    echo.
    pause
    exit /b 1
)

:: ��ȡPython�汾
for /f "tokens=*" %%v in ('"%python_path%" --version 2^>^&1') do (
    set "python_version=%%v"
)

:: ���Python�汾�Ƿ�� 3.10
echo ��⵽��װ��Python�汾: %python_version%
python -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" && (
    echo Python�汾���� �� 3.10
) || (
    echo ����: ��ҪPython �� 3.10
    pause
    exit /b 1
)

:: ���pip�Ƿ����
echo ���ڼ��pip�Ƿ����...
"%python_path%" -m pip --version > nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ����: pip������
    echo ��ȷ��Python��װ��ȷ��������: "%python_path%" -m ensurepip --upgrade
    echo.
    pause
    exit /b 1
)

:: ������⻷��ģ��
echo ���ڼ��venvģ��...
"%python_path%" -c "import venv" 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ����: venvģ�鲻����
    echo �����޸�: "%python_path%" -m ensurepip --upgrade
    echo �����°�װPython��ȷ����ѡ���п�ѡ���
    echo.
    pause
    exit /b 1
)

:: �������⻷��
set "venv_dir=venv"
if exist "%venv_dir%" (
    echo [WARN] ���⻷��Ŀ¼�Ѵ���
    choice /c YN /m "�Ƿ����´������⻷��?"
    if /i !errorlevel! == 1 (
        echo ����ɾ�������⻷��...
        rmdir /s /q "%venv_dir%"
        if exist "%venv_dir%" (
            echo.
            echo ����: �޷�ɾ�����⻷��Ŀ¼
            echo ���ֶ�ɾ�� %venv_dir% �ļ��к�����
            echo.
            pause
            exit /b 1
        ) else (
            echo ɾ���ɹ�
        )
    ) else (
        echo ʹ���������⻷��
        goto activate_venv
    )
) else (
    echo ���⻷��Ŀ¼�����ڣ��������»���
)

echo ���ڴ������⻷��...
"%python_path%" -m venv "%venv_dir%"
if %errorlevel% neq 0 (
    echo.
    echo ����: �������⻷��ʧ��
    echo ����ԭ��:
    echo 1. Ȩ�޲��� - �����Թ���Ա������д˽ű�
    echo 2. �����������ֹ - ��ʱ���÷��������
    echo 3. Python��װ�� - �����޸�Python��װ
    echo.
    pause
    exit /b 1
)

:activate_venv
:: �������⻷������װ����
echo ���ڼ������⻷��...
call "%venv_dir%\Scripts\activate.bat"
if %errorlevel% neq 0 (
    echo.
    echo ����: �޷��������⻷��
    echo ���� %venv_dir%\Scripts\activate.bat �Ƿ����
    echo.
    pause
    exit /b 1
)

:: ���requirements.txt�Ƿ����
if not exist "requirements.txt" (
    echo.
    echo ����: δ�ҵ�requirements.txt�ļ�
    echo ������������װ����
    echo.
    goto success
)

echo ���ڰ�װrequirements.txt�е�����...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo ����: ������װʧ��
    echo ��������: %venv_dir%\Scripts\python.exe -m pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

:success
echo.
echo �����������!
echo Python·��: %python_path%
echo Python�汾: %python_version%
echo ���⻷���Ѵ�����: %cd%\%venv_dir%
echo ��ǰ����Ŀ¼: %cd%

pause