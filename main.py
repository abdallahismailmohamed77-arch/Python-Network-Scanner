import socket
import sys
from datetime import datetime
import threading
from queue import Queue

# تخصيص الطابور (Queue) للبورتات
queue = Queue()
open_ports = []

def scan_port(target_ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.8)
        result = s.connect_ex((target_ip, port))
        if result == 0:
            print(f"[+] Port {port} is OPEN")
            open_ports.append(port)
        s.close()
    except:
        pass

def threader(target_ip):
    while True:
        worker = queue.get()
        scan_port(target_ip, worker)
        queue.task_done()

def main():
    print("-" * 50)
    print("Advanced Python Network Scanner - By Abdullah")
    print("-" * 50)
    
    target = input("Enter target IP to scan (e.g., 127.0.0.1): ")
    print(f"Scanning target: {target}")
    start_time = datetime.now()
    print(f"Time started: {str(start_time)}")
    print("-" * 50)

    # إنشاء 100 خيط عمل (Threads) لتسريع الفحص
    for x in range(100):
        t = threading.Thread(target=threader, args=(target,))
        t.daemon = True
        t.start()

    # وضع أول 1024 بورت في الطابور
    for worker in range(1, 1025):
        queue.put(worker)

    queue.join()
    
    print("-" * 50)
    print("Scan completed successfully!")

    # حفظ النتائج في ملف تقرير
    report_filename = "scan_report.txt"
    try:
        with open(report_filename, "w") as report_file:
            report_file.write("-" * 50 + "\n")
            report_file.write(f"Network Scan Report - Target: {target}\n")
            report_file.write(f"Time Started: {str(start_time)}\n")
            report_file.write("-" * 50 + "\n")
            if open_ports:
                for port in sorted(open_ports):
                    report_file.write(f"[+] Port {port} is OPEN\n")
            else:
                report_file.write("No open ports found.\n")
            report_file.write("-" * 50 + "\n")
        print(f"[✓] Report successfully saved as '{report_filename}'")
    except Exception as e:
        print(f"[x] Error saving report: {e}")

if __name__ == "__main__":
    main()