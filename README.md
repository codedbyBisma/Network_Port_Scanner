# Network_Port_Scanner

A Python-based command-line tool that scans a target IP for open TCP ports within a custom port range.

# Overview

Port scanning is one of the first steps in a penetration test or security audit — identifying which services are exposed on a system, similar to the basic technique used by tools like Nmap.

# How It Works

The tool takes a target IP (or localhost) and a port range, attempts a TCP connection to each port, and reports which ones are open — along with a guessed service name for common ports (like 22 = SSH, 80 = HTTP).

#Features
Scan a target IP or localhost

Custom port range support

Live progress bar during scan

Displays open ports with status and guessed service

Scan summary (ports scanned, time taken, timestamp)

Tech Stack

Python 3

socket (port connection testing)

tqdm (progress bar)

# Installation

pip install tqdm --break-system-packages

# Usage

python3 port_scanner.py

# Setup

mkdir cybertask3

cd cybertask3

Place port_scanner.py inside this folder.

#Example

Enter target IP or hostname (or 'localhost'): 192.168....

Start port (e.g. 1): 1

End port (e.g. 1024): 80

# Output:

PORT      STATUS    SERVICE (guess)

22        OPEN      SSH

# Author

Bisma — Cybersecurity Intern at SAM AI Technologies
