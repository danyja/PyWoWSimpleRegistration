import ctypes
import os
import socket
import time

import psutil
from flask import current_app


def is_process_running(process_name: str):
    """检查指定名称的进程是否已经在运行"""
    for proc in psutil.process_iter():
        try:
            if proc.name() == process_name:
                return True
            # 如果需要检查命令行参数（更严格匹配）
            # if proc.cmdline() and process_name in ' '.join(proc.cmdline()):
            #     return True
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue  # 跳过无权限访问的进程
    return False


def is_port_in_use(port: int) -> bool:
    """检查指定端口是否被占用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def close_pid(pid):
    kernel32 = ctypes.windll.kernel32
    # 1. 保存当前线程和Console状态
    original_console = kernel32.GetConsoleWindow()
    original_thread = kernel32.GetCurrentThreadId()

    try:
        # 2. 脱离当前控制台（如果当前进程有控制台）
        if original_console:
            kernel32.FreeConsole()
        # 3. 禁用当前线程的Ctrl+C处理，避免影响自己
        kernel32.SetConsoleCtrlHandler(None, True)
        # 4. 附加到目标进程的控制台
        if not kernel32.AttachConsole(pid):
            raise ctypes.WinError(ctypes.get_last_error())
        # 5. 向整个进程组发送Ctrl+C信号
        # win32con.CTRL_C_EVENT=0
        if not kernel32.GenerateConsoleCtrlEvent(0, 0):
            raise ctypes.WinError(ctypes.get_last_error())
        # 6. 等待一段时间让信号处理完成
        # win32api.Sleep(1000)
        time.sleep(1)

        return True

    except Exception as e:
        print(f"发送Ctrl+C失败: {e}")
        return False

    finally:
        # 7. 无论如何都要恢复原始状态
        kernel32.FreeConsole()

        # 重新附加到原始控制台（如果之前有）
        if original_console:
            kernel32.AttachConsole(-1)  # ATTACH_PARENT_PROCESS

        # 恢复Ctrl+C处理
        kernel32.SetConsoleCtrlHandler(None, False)


def check_status():
    status = {}
    for server in current_app.config['SERVERS']:
        status[server] = is_process_running(
            current_app.config['SERVERS'][server]["exe"])
    return status


def open_server(name, wait=1):
    # 注意通过这种方式开启的服务，在网页服务关闭后，需要先关闭这些服务器，然后再打开网页服务器，否则网页服务器将不可用。
    if not is_process_running(current_app.config['SERVERS'][name]["exe"]):
        os.chdir(current_app.config['SERVERS'][name]["path"])
        os.system("start "+current_app.config['SERVERS'][name]
                  ["exe"]+current_app.config['SERVERS'][name]["args"])
        time.sleep(wait)


def open_all():
    open_server("db")
    open_server("core")
    open_server("gate")


def close_server(name, wait=1):
    for proc in psutil.process_iter():
        try:
            if proc.name() == current_app.config['SERVERS'][name]["exe"]:
                close_pid(proc.pid)
                time.sleep(wait)
                return True
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue
    return False


def close_all():
    close_server("gate")
    close_server("core")
    close_server("db")


if __name__ == "__main__":
    print(check_status())
    open_all()
    # close_server("db")
