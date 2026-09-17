# Python TCP Port Scanner

A simple TCP port scanner made with Python and Nmap.

## Features

* Scans TCP ports
* Finds open ports
* Shows the service name
* Shows the product when available
* Allows the user to choose the port range

## Requirements

* Python 3
* Nmap
* python-nmap

## Installation

Install the Python library:

```bash
pip install python-nmap
```

Make sure Nmap is also installed.

## Usage

```bash
python port_scanner.py 192.168.1.10 20 100
```

Example output:

```text
Scanning 192.168.1.10 on ports 20-100...
Open ports:
- 192.168.1.10:22 -> ssh (OpenSSH)
- 192.168.1.10:80 -> http
```

## Purpose

This project was created to learn about Python, TCP ports, Nmap, and basic network reconnaissance.

## Disclaimer

Only scan systems that you own or have permission to test.
