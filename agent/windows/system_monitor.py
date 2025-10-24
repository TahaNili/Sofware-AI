"""
System monitoring functionality for Windows OS
"""

import psutil
import wmi
import time
from typing import Dict, List, Any, Tuple

class SystemMonitor:
    def __init__(self):
        try:
            self.wmi = wmi.WMI()
        except Exception:
            self.wmi = None
        
    def get_cpu_usage(self) -> Dict[str, Any]:
        """Get detailed CPU usage statistics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
            cpu_freq = psutil.cpu_freq()
            cpu_temp = self._get_cpu_temperature()
            
            return {
                'total_usage': psutil.cpu_percent(),
                'per_core': cpu_percent,
                'frequency': {
                    'current': cpu_freq.current if cpu_freq else 0.0,
                    'min': cpu_freq.min if cpu_freq else 0.0,
                    'max': cpu_freq.max if cpu_freq else 0.0
                },
                'temperature': cpu_temp
            }
        except Exception:
            return {
                'total_usage': 0.0,
                'per_core': [],
                'frequency': {'current': 0.0, 'min': 0.0, 'max': 0.0},
                'temperature': {}
            }
        
    def get_memory_info(self) -> Dict[str, Any]:
        """Get RAM usage statistics"""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'percent': mem.percent,
            'swap': {
                'total': swap.total,
                'used': swap.used,
                'free': swap.free,
                'percent': swap.percent
            }
        }
        
    def get_disk_info(self) -> List[Dict[str, Any]]:
        """Get disk usage information for all drives"""
        disks = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                })
            except Exception:
                continue
        return disks
        
    def get_running_processes(self) -> List[Dict[str, Any]]:
        """Get list of running processes with resource usage"""
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = proc.info
                    # Avoid potential division by zero or invalid memory calculations
                    try:
                        pinfo['cpu_percent'] = proc.cpu_percent()
                    except Exception:
                        pinfo['cpu_percent'] = 0.0
                        
                    try:
                        pinfo['memory_percent'] = proc.memory_percent()
                    except Exception:
                        pinfo['memory_percent'] = 0.0
                        
                    processes.append(pinfo)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        except Exception:
            # Return empty list if process iteration fails completely
            return []
        return processes
        
    def _get_cpu_temperature(self) -> Dict[str, float]:
        """Get CPU temperature information"""
        if not self.wmi:
            return {}
            
        try:
            temperatures = {}
            temp_query = self.wmi.MSAcpi_ThermalZoneTemperature()
            
            if not temp_query:
                return {}
                
            for item in temp_query:
                try:
                    # Convert tenths of Kelvin to Celsius
                    temp_celsius = (item.CurrentTemperature / 10.0) - 273.15
                    temperatures[f'zone_{item.InstanceName}'] = temp_celsius
                except (AttributeError, TypeError, ZeroDivisionError):
                    continue
                    
            return temperatures
        except Exception:
            return {}