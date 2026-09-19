import socket
import sys
import time
from datetime import datetime

try:
    from tqdm import tqdm
except ImportError:
    print("The 'tqdm' package is required. Install it with:")
    print("  pip install tqdm --break-system-packages")
    sys.exit(1)

# ANSI color codes (no external color library used here, on purpose —
# keeps this tool visually distinct from the other project tools)
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"

# A small reference table of common ports, used only to label results
COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 8080: "HTTP-Alt",
}


def print_banner():
    print(f"{CYAN}{'#' * 55}{RESET}")
    print(f"{CYAN}{BOLD}#{'  NETWORK PORT SCANNER'.center(53)}#{RESET}")
    print(f"{CYAN}{'#' * 55}{RESET}\n")


def resolve_target(target):
    """Resolve a hostname/IP, accepting 'localhost' as a shortcut."""
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        return None


def scan_port(ip, port, timeout=0.5):
    """Return True if the given TCP port is open on the target."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        return result == 0


def run_scan(ip, start_port, end_port):
    open_ports = []
    total_ports = end_port - start_port + 1

    print(f"\n{YELLOW}Scanning {ip} — ports {start_port} to {end_port} "
          f"({total_ports} ports){RESET}\n")

    start_time = time.time()

    for port in tqdm(range(start_port, end_port + 1),
                      desc="Scanning", unit="port",
                      bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} ports"):
        if scan_port(ip, port):
            open_ports.append(port)

    elapsed = time.time() - start_time
    return open_ports, elapsed, total_ports


def print_report(ip, open_ports, elapsed, total_scanned):
    print(f"\n{CYAN}{'-' * 55}{RESET}")
    print(f"{BOLD}SCAN SUMMARY{RESET}")
    print(f"{CYAN}{'-' * 55}{RESET}")
    print(f"Target        : {ip}")
    print(f"Ports scanned : {total_scanned}")
    print(f"Open ports    : {len(open_ports)}")
    print(f"Time taken    : {elapsed:.2f} seconds")
    print(f"Scan finished : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{CYAN}{'-' * 55}{RESET}\n")

    if not open_ports:
        print(f"{RED}No open ports found in the given range.{RESET}\n")
        return

    print(f"{BOLD}{'PORT':<10}{'STATUS':<10}{'SERVICE (guess)':<20}{RESET}")
    print("-" * 40)
    for port in open_ports:
        service = COMMON_PORTS.get(port, "Unknown")
        print(f"{GREEN}{port:<10}{'OPEN':<10}{service:<20}{RESET}")
    print()


def main():
    print_banner()

    target_input = input(f"{BOLD}Enter target IP or hostname "
                          f"(or 'localhost'): {RESET}").strip()
    if not target_input:
        print(f"{RED}No target entered. Exiting.{RESET}")
        sys.exit(1)

    ip = resolve_target(target_input)
    if not ip:
        print(f"{RED}Could not resolve '{target_input}'. Check the "
              f"hostname/IP and try again.{RESET}")
        sys.exit(1)

    try:
        start_port = int(input(f"{BOLD}Start port (e.g. 1): {RESET}").strip())
        end_port = int(input(f"{BOLD}End port (e.g. 1024): {RESET}").strip())
    except ValueError:
        print(f"{RED}Ports must be numbers.{RESET}")
        sys.exit(1)

    if start_port < 1 or end_port > 65535 or start_port > end_port:
        print(f"{RED}Invalid port range. Must be between 1-65535, "
              f"start <= end.{RESET}")
        sys.exit(1)

    open_ports, elapsed, total_scanned = run_scan(ip, start_port, end_port)
    print_report(ip, open_ports, elapsed, total_scanned)


if __name__ == "__main__":
    main()
