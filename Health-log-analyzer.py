#!/usr/bin/env python3

import re
from datetime import datetime, timedelta
from colorama import Fore, Style, init

# Initialize colorama
init()

# Configuration
LOGFILE = '/var/log/system_health.log'

def parse_log_file(logfile, start_time):
    """Parse the log file and extract relevant entries within the given time frame."""
    entries = {
        'cpu_usage': [],
        'memory_usage': [],
        'disk_usage': [],
        'top_cpu_process': [],
        'top_memory_process': [],
        'top_disk_dir': []
    }
    
    with open(logfile, 'r') as file:
        for line in file:
            date_match = re.match(r'(\w+ \w+ \d+ \d+:\d+:\d+ \d+):', line)
            if date_match:
                timestamp = datetime.strptime(date_match.group(1), '%a %b %d %H:%M:%S %Y')
            else:
                timestamp = datetime.now()

            if timestamp >= start_time:
                if 'CPU usage is high' in line:
                    cpu_usage_match = re.search(r'CPU usage is high: (\d+)%', line)
                    if cpu_usage_match:
                        cpu_usage = cpu_usage_match.group(1)
                        entries['cpu_usage'].append((timestamp, int(cpu_usage)))
                elif 'Memory usage is high' in line:
                    memory_usage_match = re.search(r'Memory usage is high: (\d+)%', line)
                    if memory_usage_match:
                        memory_usage = memory_usage_match.group(1)
                        entries['memory_usage'].append((timestamp, int(memory_usage)))
                elif 'Disk space usage is high' in line:
                    disk_usage_match = re.search(r'Disk space usage is high: (\d+)%', line)
                    if disk_usage_match:
                        disk_usage = disk_usage_match.group(1)
                        entries['disk_usage'].append((timestamp, int(disk_usage)))
                elif 'Top CPU consuming process' in line:
                    process_info_match = re.search(r'Top CPU consuming process: (\d+) (.+)', line)
                    if process_info_match:
                        pid, process_name = process_info_match.groups()
                        entries['top_cpu_process'].append((timestamp, pid, process_name))
                elif 'Top memory consuming process' in line:
                    process_info_match = re.search(r'Top memory consuming process: (\d+) (.+)', line)
                    if process_info_match:
                        pid, process_name = process_info_match.groups()
                        entries['top_memory_process'].append((timestamp, pid, process_name))
                elif 'Top disk consuming directory' in line:
                    dir_info_match = re.search(r'Top disk consuming directory: (.+)', line)
                    if dir_info_match:
                        dir_info = dir_info_match.group(1)
                        entries['top_disk_dir'].append((timestamp, dir_info))
    
    return entries

def display_summary(entries):
    """Display a summary of the log entries without repeating PIDs."""
    print(Fore.CYAN + "System Health Log Analysis" + Style.RESET_ALL)
    print(Fore.CYAN + "=========================" + Style.RESET_ALL)
    
    seen_pids_cpu = set()
    seen_pids_memory = set()
    seen_dirs = set()

    print(Fore.YELLOW + "\nHigh CPU Usage Alerts:" + Style.RESET_ALL)
    for timestamp, usage in entries['cpu_usage']:
        print(f"{Fore.GREEN}{timestamp}{Style.RESET_ALL} - CPU Usage: {Fore.RED}{usage}%{Style.RESET_ALL}")
    
    print(Fore.YELLOW + "\nTop CPU Consuming Processes:" + Style.RESET_ALL)
    for timestamp, pid, process in entries['top_cpu_process']:
        if pid not in seen_pids_cpu:
            print(f"{Fore.GREEN}{timestamp}{Style.RESET_ALL} - Process: {Fore.MAGENTA}{process}{Style.RESET_ALL} (PID: {Fore.CYAN}{pid}{Style.RESET_ALL})")
            seen_pids_cpu.add(pid)
    
    print(Fore.YELLOW + "\nHigh Memory Usage Alerts:" + Style.RESET_ALL)
    for timestamp, usage in entries['memory_usage']:
        print(f"{Fore.GREEN}{timestamp}{Style.RESET_ALL} - Memory Usage: {Fore.RED}{usage}%{Style.RESET_ALL}")
    
    print(Fore.YELLOW + "\nTop Memory Consuming Processes:" + Style.RESET_ALL)
    for timestamp, pid, process in entries['top_memory_process']:
        if pid not in seen_pids_memory:
            print(f"{Fore.GREEN}{timestamp}{Style.RESET_ALL} - Process: {Fore.MAGENTA}{process}{Style.RESET_ALL} (PID: {Fore.CYAN}{pid}{Style.RESET_ALL})")
            seen_pids_memory.add(pid)
    
    print(Fore.YELLOW + "\nHigh Disk Space Usage Alerts:" + Style.RESET_ALL)
    for timestamp, usage in entries['disk_usage']:
        print(f"{Fore.GREEN}{timestamp}{Style.RESET_ALL} - Disk Space Usage: {Fore.RED}{usage}%{Style.RESET_ALL}")
    
    print(Fore.YELLOW + "\nTop Disk Consuming Directories:" + Style.RESET_ALL)
    for timestamp, directory in entries['top_disk_dir']:
        if directory not in seen_dirs:
            print(f"{Fore.GREEN}{timestamp}{Style.RESET_ALL} - Directory: {Fore.MAGENTA}{directory}{Style.RESET_ALL}")
            seen_dirs.add(directory)

def main():
    time_frame = input("Select the time frame for analysis (1 hour, 1 day, all time): ").strip().lower()
    if time_frame == "1 hour":
        start_time = datetime.now() - timedelta(hours=1)
    elif time_frame == "1 day":
        start_time = datetime.now() - timedelta(days=1)
    elif time_frame == "all time":
        start_time = datetime.min
    else:
        print("Invalid time frame. Please choose from '1 hour', '1 day', or 'all time'.")
        return

    entries = parse_log_file(LOGFILE, start_time)
    display_summary(entries)

if __name__ == "__main__":
    main()
