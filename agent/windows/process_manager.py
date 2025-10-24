"""
Process and application management for Windows OS
"""

import os
import sys
import subprocess
import winreg
from typing import Optional, List, Dict
import psutil
import win32com.client
from pathlib import Path

class ProcessManager:
    def __init__(self):
        self.shell = win32com.client.Dispatch("WScript.Shell")
        
    def start_application(self, app_name: str) -> bool:
        """
        Start an application by name. Tries multiple methods:
        1. Direct executable name
        2. Start menu shortcut
        3. Program Files search
        """
        try:
            # Try running directly if it's an exe name
            if app_name.lower().endswith('.exe'):
                subprocess.Popen(app_name)
                return True
                
            # Try start menu shortcuts
            start_menu = self._get_start_menu_path()
            shortcuts = self._find_shortcuts(start_menu, app_name)
            
            if shortcuts:
                self.shell.Run(shortcuts[0])
                return True
                
            # Try Program Files
            program_files = self._find_in_program_files(app_name)
            if program_files:
                subprocess.Popen(program_files)
                return True
                
            return False
            
        except Exception:
            return False
            
    def stop_application(self, app_name: str) -> bool:
        """Stop a running application by name"""
        try:
            for proc in psutil.process_iter(['name']):
                if app_name.lower() in proc.info['name'].lower():
                    proc.terminate()
                    return True
            return False
        except Exception:
            return False
            
    def is_application_running(self, app_name: str) -> bool:
        """Check if an application is currently running"""
        for proc in psutil.process_iter(['name']):
            try:
                if app_name.lower() in proc.info['name'].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return False
        
    def _get_start_menu_path(self) -> str:
        """Get the path to Start Menu programs"""
        return str(Path(os.environ["APPDATA"]) / "Microsoft/Windows/Start Menu/Programs")
        
    def _find_shortcuts(self, start_dir: str, app_name: str) -> List[str]:
        """Find .lnk files matching the application name"""
        shortcuts = []
        for root, _, files in os.walk(start_dir):
            for file in files:
                if file.lower().endswith('.lnk') and app_name.lower() in file.lower():
                    shortcuts.append(os.path.join(root, file))
        return shortcuts
        
    def _find_in_program_files(self, app_name: str) -> Optional[str]:
        """Search for the application in Program Files directories"""
        search_dirs = [
            os.environ.get('ProgramFiles', 'C:/Program Files'),
            os.environ.get('ProgramFiles(x86)', 'C:/Program Files (x86)')
        ]
        
        for directory in search_dirs:
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.lower() == f"{app_name.lower()}.exe":
                        return os.path.join(root, file)
        return None
        
    def get_application_info(self, app_name: str) -> Optional[Dict[str, str]]:
        """Get information about an installed application"""
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                             r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 
                             0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                if app_name.lower() in display_name.lower():
                                    return {
                                        'name': display_name,
                                        'version': winreg.QueryValueEx(subkey, "DisplayVersion")[0],
                                        'publisher': winreg.QueryValueEx(subkey, "Publisher")[0],
                                        'install_date': winreg.QueryValueEx(subkey, "InstallDate")[0],
                                        'install_location': winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                    }
                            except (WindowsError, KeyError):
                                continue
                    except WindowsError:
                        continue
            return None
        except WindowsError:
            return None