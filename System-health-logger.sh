#!/usr/bin/env bash

# Configuration
CPU_THRESHOLD=80
MEMORY_THRESHOLD=80
DISK_THRESHOLD=80
LOGFILE="/var/log/system_health.log"

# Function to check CPU usage
check_cpu_usage() {
    local cpu_usage
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
    
    echo "CPU Usage: ${cpu_usage}%"
    
    if (( $(echo "$cpu_usage > $CPU_THRESHOLD" | bc -l) )); then
        echo "Alert: CPU usage is high: ${cpu_usage}%"
        echo "$(date): CPU usage is high: ${cpu_usage}%" >> "$LOGFILE"
    fi
    
    # Top CPU consuming process (PID and Name)
    local top_cpu_process
    top_cpu_process=$(ps aux --sort=-%cpu | awk 'NR==2 {print $2, $11}')
    echo "Top CPU consuming process: $top_cpu_process"
    echo "$(date): Top CPU consuming process: $top_cpu_process" >> "$LOGFILE"
}

# Function to check memory usage
check_memory_usage() {
    local memory_usage
    memory_usage=$(free | awk '/^Mem/ {printf("%.0f"), $3/$2 * 100.0}')
    
    echo "Memory Usage: ${memory_usage}%"
    
    if (( memory_usage > MEMORY_THRESHOLD )); then
        echo "Alert: Memory usage is high: ${memory_usage}%"
        echo "$(date): Memory usage is high: ${memory_usage}%" >> "$LOGFILE"
    fi
    
    # Top memory consuming process (PID and Name)
    local top_memory_process
    top_memory_process=$(ps aux --sort=-%mem | awk 'NR==2 {print $2, $11}')
    echo "Top memory consuming process: $top_memory_process"
    echo "$(date): Top memory consuming process: $top_memory_process" >> "$LOGFILE"
}

# Function to check disk space usage
check_disk_space() {
    local disk_usage
    disk_usage=$(df / | awk '/\// {print $5}' | sed 's/%//')
    
    echo "Disk Space Usage: ${disk_usage}%"
    
    if (( disk_usage > DISK_THRESHOLD )); then
        echo "Alert: Disk space usage is high: ${disk_usage}%"
        echo "$(date): Disk space usage is high: ${disk_usage}%" >> "$LOGFILE"
    fi
    
    # Top disk space consuming directory (Name)
    local top_disk_dir
    top_disk_dir=$(du -shx /* 2>/dev/null | sort -rh | head -n 1 | awk '{print $2}')
    echo "Top disk consuming directory: $top_disk_dir"
    echo "$(date): Top disk consuming directory: $top_disk_dir" >> "$LOGFILE"
}

# Main function to execute all checks
main() {
    echo "Starting system health check at $(date)"
    echo "Starting system health check at $(date)" >> "$LOGFILE"

    check_cpu_usage
    check_memory_usage
    check_disk_space

    echo "System health check completed at $(date)"
    echo "System health check completed at $(date)" >> "$LOGFILE"
}

# Execute the main function
main
