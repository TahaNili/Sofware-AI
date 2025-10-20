"""
Windows System Control Module
This module provides interaction capabilities with the Windows operating system
"""

import os
import sys
import subprocess
import winreg
import psutil
import win32api
import win32con
import win32gui
import win32process

class WindowsController:
    @staticmethod
    def run_program(program_name: str) -> bool:
        """
        Run a program in Windows
        """
        try:
            subprocess.Popen(program_name)
            return True
        except Exception as e:
            print(f"Error running program: {e}")
            return False

    @staticmethod
    def get_running_apps() -> list:
        """
        Get list of running applications
        """
        apps = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                apps.append({
                    'name': proc.info['name'],
                    'pid': proc.info['pid'],
                    'cpu': proc.info['cpu_percent'],
                    'memory': proc.info['memory_info'].rss / 1024 / 1024  # MB
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return apps

    @staticmethod
    def change_system_setting(setting_type: str, value: str) -> bool:
        """
        تغییر تنظیمات سیستم
        مثال: تغییر والپیپر، تنظیمات صدا و...
        """
        try:
            if setting_type == "wallpaper":
                win32gui.SystemParametersInfo(
                    win32con.SPI_SETDESKWALLPAPER, 
                    value, 
                    win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDWININICHANGE
                )
            # Additional settings can be added here
            return True
        except Exception as e:
            print(f"خطا در تغییر تنظیمات: {e}")
            return False

    @staticmethod
    def get_system_info() -> dict:
        """
        دریافت اطلاعات سیستم
        """
        info = {
            'cpu_usage': psutil.cpu_percent(interval=1),
            'memory': {
                'total': psutil.virtual_memory().total / (1024**3),  # GB
                'used': psutil.virtual_memory().used / (1024**3),    # GB
                'percent': psutil.virtual_memory().percent
            },
            'disk': {
                'total': psutil.disk_usage('/').total / (1024**3),  # GB
                'used': psutil.disk_usage('/').used / (1024**3),    # GB
                'percent': psutil.disk_usage('/').percent
            }
        }
        return info