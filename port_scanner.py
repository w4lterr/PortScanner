#!/usr/bin/env python3
"""Simple TCP port scanner using the python-nmap library."""

import argparse
import shutil
import sys

import nmap


def scan_ports(target: str, start_port: int, end_port: int, timeout: float = 3.0):
    """Scan a port range on the target and return a list of open ports."""
    if shutil.which("nmap") is None:
        raise RuntimeError("nmap executable not found in PATH. Install Nmap first.")

    scanner = nmap.PortScanner()
    port_range = f"{start_port}-{end_port}"
    arguments = f"-sT -Pn -T4 --host-timeout {int(timeout * 1000)}ms"

    result = scanner.scan(hosts=target, ports=port_range, arguments=arguments)
    hosts = result.get("scan", {})

    open_ports = []
    for host, host_data in hosts.items():
        tcp_ports = host_data.get("tcp", {})
        for port, port_data in sorted(tcp_ports.items()):
            if port_data.get("state") == "open":
                open_ports.append({
                    "host": host,
                    "port": port,
                    "state": port_data.get("state", "unknown"),
                    "name": port_data.get("name", "unknown"),
                    "product": port_data.get("product", ""),
                })

    return open_ports


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan a host for open TCP ports using nmap.")
    parser.add_argument("target", help="IP address or hostname to scan")
    parser.add_argument("start_port", type=int, help="First port in the range")
    parser.add_argument("end_port", type=int, help="Last port in the range")
    parser.add_argument("--timeout", type=float, default=3.0, help="Scanner timeout in seconds (default: 3)")
    args = parser.parse_args()

    if not (1 <= args.start_port <= 65535 and 1 <= args.end_port <= 65535):
        print("Port numbers must be between 1 and 65535.")
        return 1

    if args.start_port > args.end_port:
        print("start_port must be less than or equal to end_port.")
        return 1

    try:
        print(f"Scanning {args.target} on ports {args.start_port}-{args.end_port}...")
        open_ports = scan_ports(args.target, args.start_port, args.end_port, args.timeout)

        if not open_ports:
            print("No open ports found.")
            return 0

        print("Open ports:")
        for entry in open_ports:
            name = entry["name"]
            product = entry["product"]
            detail = f" ({product})" if product else ""
            print(f"- {entry['host']}:{entry['port']} -> {name}{detail}")
        return 0
    except RuntimeError as exc:
        print(f"Error: {exc}")
        return 1
    except Exception as exc:
        print(f"Scan failed: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
