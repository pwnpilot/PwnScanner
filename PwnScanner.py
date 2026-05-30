#!/usr/bin/env python3
"""
Network Scanner Automation Tool
Performs various nmap scans based on user selection.
Supports single IP, multiple IPs, CIDR notation, URLs, and target file input.
Authorized penetration testing use only.
"""

import subprocess
import sys
import os
import re
import socket

# Color formatting for terminal output
class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_banner():
    """Display a styled banner."""
    banner = f"""
{Color.CYAN}{Color.BOLD}

██████╗ ██╗    ██╗███╗   ██╗███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗
██╔══██╗██║    ██║████╗  ██║██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
██████╔╝██║ █╗ ██║██╔██╗ ██║███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
██╔═══╝ ██║███╗██║██║╚██╗██║╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
██║     ╚███╔███╔╝██║ ╚████║███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
╚═╝      ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝

                Offensive Security • Reconnaissance • Enumeration

{Color.GREEN}Author  : ABHISHEK KUMAR SINGH{Color.END}
{Color.GREEN}Version : 1.0{Color.END}

{Color.END}
{Color.WARNING}[!] Authorized Penetration Testing Only{Color.END}
"""
    print(banner)

def print_footer():
    """Display a footer with author and tool info."""
    footer = f"""
{Color.WARNING}{'='*60}{Color.END}
{Color.CYAN}{Color.BOLD}   PwnScanner by PwnPilot | github.com/PwnPilot{Color.END}
{Color.WARNING}{'='*60}{Color.END}
    """
    print(footer)

def check_nmap():
    """Verify nmap is installed."""
    try:
        subprocess.run(["nmap", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{Color.RED}[!] Nmap is not installed. Install it with: sudo apt install nmap{Color.END}")
        return False

def resolve_url_to_host(url):
    """Extract hostname from a URL and optionally resolve it to an IP."""
    url = url.strip()

    # Strip protocol prefix
    hostname = url
    for prefix in ['https://', 'http://', 'ftp://', 'socks4://', 'socks5://']:
        if hostname.lower().startswith(prefix):
            hostname = hostname[len(prefix):]
            break

    # Strip path, query params, fragments
    if '/' in hostname:
        hostname = hostname.split('/')[0]
    if '?' in hostname:
        hostname = hostname.split('?')[0]
    if '#' in hostname:
        hostname = hostname.split('#')[0]

    # Strip port if present
    if ':' in hostname and not hostname.replace('.', '').replace(':', '').isdigit():
        # Only strip port if we're not dealing with IPv6
        parts = hostname.rsplit(':', 1)
        if parts[1].isdigit():
            hostname = parts[0]

    return hostname

def resolve_host_to_ip(hostname):
    """Try to resolve a hostname to an IP address."""
    try:
        ip = socket.gethostbyname(hostname)
        return ip
    except socket.gaierror:
        return None

def get_target():
    """Get target in any supported format from user."""
    print(f"""
{Color.CYAN}Target Input Options:{Color.END}
  {Color.GREEN}1.{Color.END} Single IP              - 192.168.1.1
  {Color.GREEN}2.{Color.END} Multiple IPs            - 192.168.1.1 192.168.1.2 10.0.0.5
  {Color.GREEN}3.{Color.END} CIDR Notation           - 192.168.1.0/24
  {Color.GREEN}4.{Color.END} IP Range                - 192.168.1.1-100
  {Color.GREEN}5.{Color.END} URL / Hostname          - example.com  or  https://example.com/path
  {Color.GREEN}6.{Color.END} Multiple URLs/Hosts     - example.com scanme.nmap.org
  {Color.GREEN}7.{Color.END} Load from text file     - targets.txt (one target per line)
  {Color.GREEN}8.{Color.END} Wildcard notation       - 192.168.1.*
""")

    raw = input(f"{Color.BOLD}[+] Enter target(s): {Color.END}").strip()

    if not raw:
        print(f"{Color.RED}[!] Target cannot be empty.{Color.END}")
        sys.exit(1)

    # ── File input ──────────────────────────────────────────────────
    if raw.endswith('.txt'):
        if not os.path.exists(raw):
            print(f"{Color.RED}[!] File '{raw}' not found.{Color.END}")
            sys.exit(1)
        try:
            with open(raw, 'r') as f:
                lines = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
            if not lines:
                print(f"{Color.RED}[!] File '{raw}' is empty or has no valid targets.{Color.END}")
                sys.exit(1)
            # Process each line for URLs
            processed = []
            for line in lines:
                if any(line.lower().startswith(p) for p in ['http://', 'https://', 'ftp://']) or \
                   '.' in line and not re.match(r'^\d+\.\d+\.\d+\.\d+', line) and '/' not in line.replace('://', ''):
                    host = resolve_url_to_host(line)
                    ip = resolve_host_to_ip(host)
                    if ip:
                        print(f"{Color.CYAN}    URL resolved: {line} -> {host} ({ip}){Color.END}")
                        processed.append(ip)
                    else:
                        print(f"{Color.WARNING}    [!] Could not resolve {line}, using as-is{Color.END}")
                        processed.append(host)
                else:
                    processed.append(line)
            print(f"{Color.GREEN}[+] Loaded {len(processed)} target(s) from '{raw}':{Color.END}")
            for i, t in enumerate(processed, 1):
                print(f"     {Color.CYAN}{i}. {t}{Color.END}")
            return processed
        except Exception as e:
            print(f"{Color.RED}[!] Error reading file '{raw}': {e}{Color.END}")
            sys.exit(1)

    # ── Split into individual tokens ───────────────────────────────
    tokens = raw.replace(',', ' ').split()
    tokens = [t.strip() for t in tokens if t.strip()]

    processed_targets = []

    for token in tokens:
        # Check if it looks like a URL (contains :// or common TLD pattern)
        is_url = any(token.lower().startswith(p) for p in ['http://', 'https://', 'ftp://'])
        is_hostname = not is_url and '.' in token and not re.match(r'^\d+\.\d+\.\d+\.\d+', token) \
                      and not token.startswith('*') and not token.endswith('*') \
                      and '/' not in token and '-' not in token.replace(':', '').split('/')[0]

        if is_url or is_hostname:
            host = resolve_url_to_host(token)
            ip = resolve_host_to_ip(host)
            if ip:
                print(f"{Color.GREEN}    [+] {token} resolved to {ip}{Color.END}")
                processed_targets.append(ip)
            else:
                print(f"{Color.WARNING}    [!] Could not resolve '{host}', using hostname directly{Color.END}")
                processed_targets.append(host)
        else:
            processed_targets.append(token)

    if len(processed_targets) == 1:
        print(f"{Color.GREEN}[+] Single target: {processed_targets[0]}{Color.END}")
    else:
        print(f"{Color.GREEN}[+] {len(processed_targets)} target(s):{Color.END}")
        for i, t in enumerate(processed_targets, 1):
            print(f"     {Color.CYAN}{i}. {t}{Color.END}")

    return processed_targets

def run_nmap(command, description):
    """Execute an nmap command and display output in real-time."""
    print(f"\n{Color.BOLD}{Color.BLUE}[*] Running: {description}{Color.END}")
    print(f"{Color.CYAN}[*] Command: nmap {' '.join(command)}{Color.END}\n")
    print(f"{Color.WARNING}{'='*60}{Color.END}")

    try:
        process = subprocess.Popen(
            ["nmap"] + command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        for line in process.stdout:
            print(line, end='')
        process.wait()
        if process.returncode != 0:
            print(f"\n{Color.RED}[!] Scan completed with warnings/errors (exit code: {process.returncode}){Color.END}")
        else:
            print(f"\n{Color.GREEN}[+] Scan completed successfully.{Color.END}")
    except Exception as e:
        print(f"{Color.RED}[!] Error running scan: {e}{Color.END}")

    print(f"{Color.WARNING}{'='*60}{Color.END}")
    print_footer()

def save_results(targets, command, description):
    """Ask user if they want to save results to a file."""
    save = input(f"\n{Color.BOLD}[?] Save results to file? (y/n): {Color.END}").strip().lower()
    if save == 'y':
        first = targets[0] if isinstance(targets, list) else targets
        safe = first.replace('/', '_slash_').replace('.', '_').replace(':', '_').replace('*', 'wildcard')
        if len(targets) > 1:
            safe += f"_plus{len(targets)-1}more"
        filename = f"PwnScanner_scan_{safe}_{description.replace(' ', '_')}.txt"
        try:
            with open(filename, 'w') as f:
                f.write(f"# PwnScanner - Scan Results\n")
                f.write(f"# Author: PwnPilot\n")
                if isinstance(targets, list):
                    f.write(f"# Targets ({len(targets)}):\n")
                    for t in targets:
                        f.write(f"#   - {t}\n")
                else:
                    f.write(f"# Target: {targets}\n")
                f.write(f"# Scan Type: {description}\n")
                f.write(f"# Command: nmap {' '.join(command)}\n")
                f.write(f"{'#'*60}\n\n")
                result = subprocess.run(["nmap"] + command, capture_output=True, text=True)
                f.write(result.stdout)
                if result.stderr:
                    f.write("\n[STDERR]\n" + result.stderr)
                f.write(f"\n# Scan completed by PwnScanner\n")
            print(f"{Color.GREEN}[+] Results saved to: {filename}{Color.END}")
        except Exception as e:
            print(f"{Color.RED}[!] Error saving file: {e}{Color.END}")

# ─── Scan Modules ──────────────────────────────────────────────────────

def host_discovery(targets):
    """Host Discovery scans."""
    print(f"\n{Color.BOLD}{Color.HEADER}{'='*60}{Color.END}")
    print(f"{Color.BOLD}{Color.HEADER}      HOST DISCOVERY SCANS — PwnScanner{Color.END}")
    print(f"{Color.BOLD}{Color.HEADER}{'='*60}{Color.END}")

    target_str = ' '.join(targets) if isinstance(targets, list) else targets

    print(f"""
{Color.CYAN}Select Host Discovery Method:{Color.END}
{Color.GREEN}[1]{Color.END} Ping Sweep (ICMP Echo)           - nmap -sn -PE {target_str}
{Color.GREEN}[2]{Color.END} TCP SYN Ping (port 80,443)        - nmap -sn -PS80,443 {target_str}
{Color.GREEN}[3]{Color.END} TCP ACK Ping (port 80)            - nmap -sn -PA80 {target_str}
{Color.GREEN}[4]{Color.END} UDP Ping (port 53)                - nmap -sn -PU53 {target_str}
{Color.GREEN}[5]{Color.END} ARP Scan (local network)          - nmap -sn -PR {target_str}
{Color.GREEN}[6]{Color.END} No ping (assume host is up)       - nmap -Pn {target_str}
{Color.GREEN}[7]{Color.END} DNS Resolution Check Only         - no nmap, just resolve hostnames
{Color.GREEN}[0]{Color.END} Back to main menu
""")

    choice = input(f"{Color.BOLD}[?] Select option [0-7]: {Color.END}").strip()

    if choice == '7':
        print(f"\n{Color.BOLD}{Color.BLUE}[*] Resolving hostnames...{Color.END}")
        for t in targets:
            ip = resolve_host_to_ip(t)
            if ip:
                print(f"  {Color.GREEN}{t} -> {ip}{Color.END}")
            else:
                print(f"  {Color.RED}{t} -> [UNRESOLVABLE]{Color.END}")
        print()
        return

    commands = {
        '1': (["-sn", "-PE"] + targets, "ICMP Echo Ping Sweep"),
        '2': (["-sn", "-PS80,443"] + targets, "TCP SYN Ping (ports 80,443)"),
        '3': (["-sn", "-PA80"] + targets, "TCP ACK Ping (port 80)"),
        '4': (["-sn", "-PU53"] + targets, "UDP Ping (port 53)"),
        '5': (["-sn", "-PR"] + targets, "ARP Scan"),
        '6': (["-Pn"] + targets, "No Ping (Treat all hosts as up)"),
    }

    if choice in commands:
        cmd, desc = commands[choice]
        run_nmap(cmd, desc)
        save_results(targets, cmd, desc)
    elif choice == '0':
        return
    else:
        print(f"{Color.RED}[!] Invalid option.{Color.END}")

def port_scanning(targets):
    """Port Scanning techniques."""
    print(f"\n{Color.BOLD}{Color.HEADER}{'='*60}{Color.END}")
    print(f"{Color.BOLD}{Color.HEADER}      PORT SCANNING — PwnScanner{Color.END}")
    print(f"{Color.BOLD}{Color.HEADER}{'='*60}{Color.END}")

    target_str = ' '.join(targets) if isinstance(targets, list) else targets

    print(f"""
{Color.CYAN}Select Port Scan Type:{Color.END}
{Color.GREEN}[1]{Color.END} SYN Stealth Scan (default)        - nmap -sS {target_str}
{Color.GREEN}[2]{Color.END} TCP Connect Scan                   - nmap -sT {target_str}
{Color.GREEN}[3]{Color.END} UDP Scan                           - nmap -sU {target_str}
{Color.GREEN}[4]{Color.END} FIN Scan                           - nmap -sF {target_str}
{Color.GREEN}[5]{Color.END} Xmas Scan                          - nmap -sX {target_str}
{Color.GREEN}[6]{Color.END} Null Scan                          - nmap -sN {target_str}
{Color.GREEN}[7]{Color.END} ACK Scan (firewall mapping)        - nmap -sA {target_str}
{Color.GREEN}[8]{Color.END} Window Scan                        - nmap -sW {target_str}
{Color.GREEN}[9]{Color.END} Maimon Scan                        - nmap -sM {target_str}
{Color.GREEN}[10]{Color.END} Scan all 65535 ports               - nmap -p- {target_str}
{Color.GREEN}[11]{Color.END} Scan top 100 ports                - nmap --top-ports 100 {target_str}
{Color.GREEN}[12]{Color.END} Scan common ports (1-1000)        - nmap -p 1-1000 {target_str}
{Color.GREEN}[13]{Color.END} HTTP/HTTPS ports only (80,443)    - nmap -p 80,443 {target_str}
{Color.GREEN}[14]{Color.END} Custom port range                 - nmap -p <PORTS> {target_str}
{Color.GREEN}[0]{Color.END} Back to main menu
""")

    choice = input(f"{Color.BOLD}[?] Select option [0-14]: {Color.END}").strip()

    commands = {
        '1': (["-sS"] + targets, "SYN Stealth Scan"),
        '2': (["-sT"] + targets, "TCP Connect Scan"),
        '3': (["-sU", "--top-ports", "100"] + targets, "UDP Scan (top 100 ports)"),
        '4': (["-sF"] + targets, "FIN Scan"),
        '5': (["-sX"] + targets, "Xmas Scan"),
        '6': (["-sN"] + targets, "Null Scan"),
        '7': (["-sA"] + targets, "ACK Scan (Firewall Mapping)"),
        '8': (["-sW"] + targets, "Window Scan"),
        '9': (["-sM"] + targets, "Maimon Scan"),
        '10': (["-p-"] + targets, "Full Port Scan (all 65535 ports)"),
        '11': (["--top-ports", "100"] + targets, "Top 100 Ports Scan"),
        '12': (["-p", "1-1000"] + targets, "Common Ports (1-1000)"),
        '13': (["-p", "80,443"] + targets, "HTTP/HTTPS Ports (80, 443)"),
    }

    if choice in commands:
        cmd, desc = commands[choice]
        run_nmap(cmd, desc)
        save_results(targets, cmd, desc)
    elif choice == '14':
        ports = input(f"{Color.BOLD}[+] Enter port(s) (e.g., 22,80,443 or 1-5000): {Color.END}").strip()
        if ports:
            cmd = ["-p", ports] + targets
            run_nmap(cmd, f"Custom Port Scan ({ports})")
            save_results(targets, cmd, f"Custom_Port_Scan_{ports}")
    elif choice == '0':
        return
    else:
        print(f"{Color.RED}[!] Invalid option.{Color.END}")

def service_discovery(targets):
    """Service and Version Detection."""
    print(f"\n{Color.BOLD}{Color.HEADER}{'='*60}{Color.END}")
    print(f"{Color.BOLD}{Color.HEADER}      SERVICE DISCOVERY — PwnScanner{Color.END}")
    print(f"{Color.BOLD}{Color.HEADER}{'='*60}{Color.END}")

    target_str = ' '.join(targets) if isinstance(targets, list) else targets

    print(f"""
{Color.CYAN}Select Service Discovery Method:{Color.END}
{Color.GREEN}[1]{Color.END} Basic Version Detection            - nmap -sV {target_str}
{Color.GREEN}[2]{Color.END} Version Detection (intensity 9)     - nmap -sV --version-intensity 9 {target_str}
{Color.GREEN}[3]{Color.END} Light Version Detection             - nmap -sV --version-light {target_str}
{Color.GREEN}[4]{Color.END} Service & OS Detection              - nmap -A {target_str}
{Color.GREEN}[5]{Color.END} Service + Script Scan               - nmap -sC -sV {target_str}
{Color.GREEN}[6]{Color.END} Aggressive All-in-One               - nmap -A -T4 {target_str}
{Color.GREEN}[7]{Color.END} NSE Vulnerability Scan              - nmap -sV --script vuln {target_str}
{Color.GREEN}[8]{Color.END} NSE Safe Scripts                    - nmap -sV --script "safe" {target_str}
{Color.GREEN}[9]{Color.END} HTTP Service Enumeration            - nmap -sV --script http-enum {target_str}
{Color.GREEN}[0]{Color.END} Back to main menu
""")

    choice = input(f"{Color.BOLD}[?] Select option [0-9]: {Color.END}").strip()

    commands = {
        '1': (["-sV"] + targets, "Basic Version Detection"),
        '2': (["-sV", "--version-intensity", "9"] + targets, "Version Detection (Intensity 9)"),
        '3': (["-sV", "--version-light"] + targets, "Light Version Detection"),
        '4': (["-A"] + targets, "Service & OS Detection (-A)"),
        '5': (["-sC", "-sV"] + targets, "Service + Default Scripts"),
        '6': (["-A", "-T4"] + targets, "Aggressive All-in-One"),
        '7': (["-sV", "--script", "vuln"] + targets, "NSE Vulnerability Scan"),
        '8': (["-sV", "--script", "safe"] + targets, "NSE Safe Scripts Scan"),
        '9': (["-sV", "--script", "http-enum"] + targets, "HTTP Service Enumeration"),
    }

    if choice in commands:
        cmd, desc = commands[choice]
        run_nmap(cmd, desc)
        save_results(targets, cmd, desc)
    elif choice == '0':
        return
    else:
        print(f"{Color.RED}[!] Invalid option.{Color.END}")

def os_discovery(targets):
    """OS Detection."""
    print(f"\n{Color.BOLD}{Color.HEADER}{'='*60}{Color.END}")
    print(f"{Color.BOLD}{Color.HEADER}      OPERATING SYSTEM DISCOVERY — PwnScanner{Color.END}")
    print(f"{Color.BOLD}{Color.HEADER}{'='*60}{Color.END}")

    target_str = ' '.join(targets) if isinstance(targets, list) else targets

    print(f"""
{Color.CYAN}Select OS Discovery Method:{Color.END}
{Color.GREEN}[1]{Color.END} Basic OS Detection                 - nmap -O {target_str}
{Color.GREEN}[2]{Color.END} OS Detection (verbose)              - nmap -O -v {target_str}
{Color.GREEN}[3]{Color.END} OS Detection with Version           - nmap -O -sV {target_str}
{Color.GREEN}[4]{Color.END} Aggressive OS Detection             - nmap -A {target_str}
{Color.GREEN}[5]{Color.END} OS Detection (limit to best guess)  - nmap -O --osscan-limit {target_str}
{Color.GREEN}[6]{Color.END} OS Detection (max guesses)          - nmap -O --max-os-tries 1 {target_str}
{Color.GREEN}[0]{Color.END} Back to main menu
""")

    choice = input(f"{Color.BOLD}[?] Select option [0-6]: {Color.END}").strip()

    commands = {
        '1': (["-O"] + targets, "Basic OS Detection"),
        '2': (["-O", "-v"] + targets, "OS Detection (Verbose)"),
        '3': (["-O", "-sV"] + targets, "OS + Version Detection"),
        '4': (["-A"] + targets, "Aggressive (OS + Version + Scripts)"),
        '5': (["-O", "--osscan-limit"] + targets, "OS Detection (Limited)"),
        '6': (["-O", "--max-os-tries", "1"] + targets, "OS Detection (Fast - 1 Try)"),
    }

    if choice in commands:
        cmd, desc = commands[choice]
        run_nmap(cmd, desc)
        save_results(targets, cmd, desc)
    elif choice == '0':
        return
    else:
        print(f"{Color.RED}[!] Invalid option.{Color.END}")

def firewall_evasion(targets):
    """Scanning beyond firewalls / evasion techniques."""
    print(f"\n{Color.BOLD}{Color.HEADER}{'='*60}{Color.END}")
    print(f"{Color.BOLD}{Color.HEADER}      FIREWALL EVASION / BYPASS — PwnScanner{Color.END}")
    print(f"{Color.BOLD}{Color.HEADER}{'='*60}{Color.END}")

    target_str = ' '.join(targets) if isinstance(targets, list) else targets

    print(f"""
{Color.CYAN}Select Evasion Technique:{Color.END}
{Color.GREEN}[1]{Color.END} Fragment Packets (min MTU)          - nmap -f {target_str}
{Color.GREEN}[2]{Color.END} Custom MTU fragmentation           - nmap --mtu 32 {target_str}
{Color.GREEN}[3]{Color.END} Decoy Scan (spoofed sources)        - nmap -D RND:10 {target_str}
{Color.GREEN}[4]{Color.END} Idle Zombie Scan                    - nmap -sI <ZOMBIE> {target_str}
{Color.GREEN}[5]{Color.END} Spoof Source IP                     - nmap -S <IP> {target_str}
{Color.GREEN}[6]{Color.END} Source Port Spoof (port 53)         - nmap -g 53 {target_str}
{Color.GREEN}[7]{Color.END} Append Random Data to Packets       - nmap --data-length 200 {target_str}
{Color.GREEN}[8]{Color.END} Slow Scan (paranoid timing)         - nmap -T0 {target_str}
{Color.GREEN}[9]{Color.END} Randomize Target Order              - nmap --randomize-hosts {target_str}
{Color.GREEN}[10]{Color.END} Spoof MAC Address                   - nmap --spoof-mac 00:11:22:33:44:55 {target_str}
{Color.GREEN}[11]{Color.END} Proxy Scan (SOCKS4)                 - nmap --proxies socks4://127.0.0.1:9050 {target_str}
{Color.GREEN}[12]{Color.END} Combo Evasion (slow + frag + data)  - nmap -T1 -f --data-length 200 {target_str}
{Color.GREEN}[13]{Color.END} Custom Evasion Options              - Enter your own flags
{Color.GREEN}[0]{Color.END} Back to main menu
""")

    choice = input(f"{Color.BOLD}[?] Select option [0-13]: {Color.END}").strip()

    commands = {
        '1': (["-f"] + targets, "Fragment Packets (8 bytes)"),
        '2': (["--mtu", "32"] + targets, "Custom MTU (32 bytes)"),
        '3': (["-D", "RND:10"] + targets, "Decoy Scan (10 random decoys)"),
        '5': (["-S", "<SPOOFED_IP>"] + targets, "Spoof Source IP"),
        '6': (["-g", "53"] + targets, "Source Port 53 (DNS)"),
        '7': (["--data-length", "200"] + targets, "Append Random Data (200 bytes)"),
        '8': (["-T0"] + targets, "Paranoid Timing (Slow)"),
        '9': (["--randomize-hosts"] + targets, "Randomize Host Order"),
        '10': (["--spoof-mac", "00:11:22:33:44:55"] + targets, "Spoofed MAC Address"),
        '12': (["-T1", "-f", "--data-length", "200"] + targets, "Combo Evasion (Slow+Frag+Data)"),
    }

    if choice == '4':
        zombie = input(f"{Color.BOLD}[+] Enter zombie IP: {Color.END}").strip()
        if zombie:
            cmd = ["-sI", zombie] + targets
            run_nmap(cmd, f"Idle Zombie Scan (Zombie: {zombie})")
            save_results(targets, cmd, f"Zombie_Scan_{zombie}")
    elif choice == '11':
        proxy = input(f"{Color.BOLD}[+] Enter proxy URL (e.g., socks4://127.0.0.1:9050): {Color.END}").strip()
        if proxy:
            cmd = ["--proxies", proxy] + targets
            run_nmap(cmd, f"Proxy Scan via {proxy}")
            save_results(targets, cmd, "Proxy_Scan")
    elif choice == '13':
        extra = input(f"{Color.BOLD}[+] Enter additional nmap flags (e.g., -sS -T2 -f --data-length 100): {Color.END}").strip()
        if extra:
            cmd = extra.split() + targets
            run_nmap(cmd, f"Custom Evasion: {extra}")
            save_results(targets, cmd, "Custom_Evasion")
    elif choice in commands:
        cmd, desc = commands[choice]
        run_nmap(cmd, desc)
        save_results(targets, cmd, desc)
    elif choice == '0':
        return
    else:
        print(f"{Color.RED}[!] Invalid option.{Color.END}")

def show_menu():
    """Display the main menu."""
    print(f"""
{Color.BOLD}{Color.HEADER}{'='*60}{Color.END}
{Color.BOLD}{Color.HEADER}         MAIN MENU — PwnScanner{Color.END}
{Color.BOLD}{Color.HEADER}{'='*60}{Color.END}

{Color.GREEN}[1]{Color.END} Host Discovery (Ping Sweeps)
{Color.GREEN}[2]{Color.END} Port Scanning
{Color.GREEN}[3]{Color.END} Service Discovery (Version Detection)
{Color.GREEN}[4]{Color.END} OS Discovery (Fingerprinting)
{Color.GREEN}[5]{Color.END} Firewall Evasion / Bypass
{Color.GREEN}[6]{Color.END} Run ALL with Aggressive (-A -T4)
{Color.RED}[0]{Color.END} Exit
""")

def run_aggressive_all(targets):
    """Run an aggressive all-in-one scan."""
    print(f"\n{Color.BOLD}{Color.WARNING}[*] Running Aggressive All-in-One Scan...{Color.END}")
    print(f"{Color.WARNING}[*] This includes: Host Disc, Port Scan, Service Ver, OS Detect, NSE Scripts{Color.END}")
    cmd = ["-A", "-T4"] + targets
    run_nmap(cmd, "Aggressive All-in-One (-A -T4)")
    save_results(targets, cmd, "Aggressive_All-In-One")

def main():
    """Main entry point."""
    print_banner()
    print_footer()

    if not check_nmap():
        sys.exit(1)

    targets = get_target()

    while True:
        show_menu()
        choice = input(f"{Color.BOLD}[?] Select option [0-6]: {Color.END}").strip()

        actions = {
            '1': lambda: host_discovery(targets),
            '2': lambda: port_scanning(targets),
            '3': lambda: service_discovery(targets),
            '4': lambda: os_discovery(targets),
            '5': lambda: firewall_evasion(targets),
            '6': lambda: run_aggressive_all(targets),
            '0': lambda: sys.exit(0),
        }

        action = actions.get(choice)
        if action:
            action()
        else:
            print(f"{Color.RED}[!] Invalid option. Please select 0-6.{Color.END}")

        if choice != '0':
            input(f"\n{Color.BOLD}[+] Press Enter to continue...{Color.END}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Color.RED}[!] Scan interrupted by user. Exiting.{Color.END}")
        sys.exit(0)