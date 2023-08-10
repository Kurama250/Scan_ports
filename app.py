# Created by Kurama
# Github: https://github.com/Kurama250
# Scan IP v1.1

import os
import tqdm
import socket
import concurrent.futures
import sys

def check_module(module_name):
    try:
        __import__(module_name)
    except ImportError:
        print(f"Module '{module_name}' not found. Install with: pip install {module_name}")
        sys.exit(1)

check_module("os")
check_module("tqdm")
check_module("socket")
check_module("concurrent.futures")
check_module("sys")

MAX_THREADS = 100  # Nombre maximum de threads simultanés pour le scan

def create_directory():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    scan_directory = os.path.join(script_directory, "scan")
    if not os.path.exists(scan_directory):
        print("Creating 'scan' directory ...")
        os.makedirs(scan_directory)
        print("Directory 'scan' created.")
    else:
        print("Directory 'scan' already exists.")

def write_ports(protocol, open_ports):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    filename = f"scan-{protocol}.txt"
    filepath = os.path.join(script_directory, "scan", filename)
    mode = "a" if os.path.exists(filepath) and len(open_ports) > 0 else "w"
    with open(filepath, mode) as file:
        if len(open_ports) > 0:
            if mode == "w":
                file.write(f"Open {protocol.upper()} ports:\n")
            for port in open_ports:
                file.write(f"{port}\n")
        else:
            file.write("All close ports\n")

def port_open(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex((ip, port))
        return result == 0

def udp_scan(ip):
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [executor.submit(port_open, ip, port) for port in range(1, 65001)]
        for future in tqdm.tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Scanning UDP "):
            port = 1 + futures.index(future)
            if future.result():
                open_ports.append(port)

    return open_ports

def tcp_scan(ip):
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [executor.submit(port_open, ip, port) for port in range(1, 65001)]
        for future in tqdm.tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Scanning TCP "):
            port = 1 + futures.index(future)
            if future.result():
                open_ports.append(port)

    return open_ports

def scan_ip(ip):
    create_directory()
    udp_ports = udp_scan(ip)
    write_ports("udp", udp_ports)

    tcp_ports = tcp_scan(ip)
    write_ports("tcp", tcp_ports)

def main():
    print(
        "   /\ /\_   _ _ __ __ _ _ __ ___   __ _   \n"
        "  / //_/ | | | '__/ _\` | '_ \` _\ / _\|  \n"
        " / __ \| |_| | | | (_| | | | | | | (_| |  \n"
        " \/  \/ \__,_|_|  \__,_|_| |_| |_|\__,_|  \n"
        "                                          \n"
        "         Created by Kurama250             \n"
        "   Github: https://github.com/Kurama250   \n"
        "             Scan IP v1.1                 \n"
    )
    ip = input("Please enter the IP address to scan: ")
    print("\nStarting the scan in progress ...")
    try:
        scan_ip(ip)
        print("Scan completed successfully.")
    except Exception as e:
        print(f"Scan error: {e}")

if __name__ == "__main__":
    main()
    input("Press Enter to exit ...")
