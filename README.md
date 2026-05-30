**PwnScanner**

An interactive Nmap automation toolkit for network reconnaissance and penetration testing.


**Overview**

<img width="721" height="213" alt="image" src="https://github.com/user-attachments/assets/8cbbfdb7-a6d7-4734-8a44-88b685613469" />


PwnScanner is a powerful, menu-driven Python wrapper around Nmap that streamlines network scanning operations. It provides an interactive interface to execute the full spectrum of Nmap scanning techniques without remembering complex command-line flags.

Built for penetration testers, network administrators, and security professionals who need quick, repeatable, and comprehensive network scans.

**Features**

**1. Host Discovery**

Detect live hosts on a target network using various probe techniques.



Option	Technique	Nmap Command

ICMP Echo Sweep	Standard ping sweep	nmap -sn -PE <target>

TCP SYN Ping	SYN probes on ports 80,443	nmap -sn -PS80,443 <target>

TCP ACK Ping	ACK probes on port 80	nmap -sn -PA80 <target>

UDP Ping	UDP probe on port 53	nmap -sn -PU53 <target>

ARP Scan	ARP requests (local subnet)	nmap -sn -PR <target>

No Ping	Treat all hosts as up	nmap -Pn <target>

DNS Resolution	Hostname-to-IP lookup only	No Nmap (uses socket)

**2. Port Scanning**

Comprehensive port detection across all major scan types.



Option	Scan Type	Characteristics

SYN Stealth	Half-open TCP	Fast, stealthy, default

TCP Connect	Full handshake	Complete connection, less stealthy

UDP Scan	UDP probes	Detects UDP services

FIN Scan	FIN flags	Bypasses some firewalls

Xmas Scan	FIN+PSH+URG	TCP header manipulation

Null Scan	No flags set	Firewall evasion

ACK Scan	ACK flags	Maps firewall rulesets
Window Scan	Window field analysis	Refined firewall mapping

Maimon Scan	FIN+ACK	Niche evasion technique

Full Scan	All 65,535 ports	Complete coverage (slow)

Top 100	Most common ports	Quick reconnaissance

Common Ports 1-1000	Standard range	Balanced speed/coverage

HTTP/HTTPS	Ports 80, 443	Web server focus

Custom Range	User-defined	Flexible targeting

**3. Service Discovery (Version Detection)**

Identify running services and their software versions.


Option	Technique	Use Case

Basic Version	-sV	Standard service identification

Intensity 9	Deep probe	Maximum version accuracy

Light Version	Quick check	Speed over detail

Service + Scripts	-sC -sV	Info gathering combo

Aggressive All	-A -T4	Full reconnaissance

NSE Vulnerability	--script vuln	Known CVE checks

NSE Safe Scripts	--script safe	Non-intrusive enumeration

HTTP Enumeration	--script http-enum	Web directory/endpoint discovery

**4. OS Discovery (Fingerprinting)**

Identify target operating systems via TCP/IP stack analysis.


Option	Description

Basic OS Detection	Default fingerprinting

Verbose OS Detection	Detailed probe output

OS + Version	Combined service + OS

Aggressive -A	Full suite including OS

Limit Best Guess	Single best match

Fast (1 Try)	Quick, single attempt

**5. Firewall Evasion / Bypass**

Techniques to circumvent network security controls.

Option	Technique	Nmap Flags

Packet Fragmentation	Fragment IP packets	-f

Custom MTU	Small packet size	--mtu 32

Decoy Scan	Spoofed source addresses	-D RND:10

Idle Zombie	Blind scan via zombie host	-sI <zombie>

Source IP Spoof	Fake source address	-S <IP>

Source Port 53	DNS port spoofing	-g 53

Random Data Padding	Append junk bytes	--data-length 200

Paranoid Timing	Extremely slow	-T0

Randomize Targets	Shuffle host order	--randomize-hosts

MAC Spoofing	Fake MAC address	--spoof-mac <mac>

Proxy Scanning	Route via SOCKS4 proxy	--proxies socks4://...

Combo Evasion	Slow + Frag + Data	Full stealth stack

Custom Flags	User-defined	Full flexibility

**6. Aggressive All-in-One**

nmap -A -T4 <target> — Host discovery, port scanning, service versioning, OS detection, and NSE default scripts in a single pass.

Supported Target Formats

**PwnScanner intelligently handles all standard target formats:**

Format	Example	Description

Single IP	192.168.1.1	One host

Multiple IPs	192.168.1.1 192.168.1.2	Space-separated

CIDR Notation	192.168.1.0/24	Subnet range

IP Range	192.168.1.1-100	Sequential range

Hostname	example.com	DNS-resolved

URL	https://example.com/path	Auto-strips protocol/path

Mixed	192.168.1.1 example.com 10.0.0.0/28	Any combination

Text File	targets.txt	One target per line

Wildcard	192.168.1.*	Nmap wildcard expansion

Note: URLs and hostnames are automatically resolved to IP addresses before being passed to Nmap. The script displays the resolution result for transparency.

**Installation**

Prerequisites: Python 3.6+

Nmap (install via package manager)

Install Nmap

bash



# Debian / Ubuntu / Kali Linux

sudo apt update && sudo apt install nmap -y

# Arch Linux

sudo pacman -S nmap

# macOS (Homebrew)

brew install nmap

# Windows

# Download from: https://nmap.org/download.html

Download PwnScanner

bash



# Clone the repository

git clone https://github.com/PwnPilot/PwnScanner.git

# Navigate to directory

cd PwnScanner

# Make executable (optional)

chmod +x PwnScanner.py

Usage

bash



sudo python3 PwnScanner.py

Note: Many scan types (SYN scan, OS detection, fragmentation) require root privileges. Run with sudo for full functionality.

Interactive Workflow



1. Launch the tool

2. Enter target(s) at the prompt

3. Select scan category from main menu

4. Choose specific scan technique

5. View real-time Nmap output

6. Optionally save results to file

7. Return to main menu for additional scans


**Example Session**

**bash**

$ sudo python3 PwnScanner.py

[*] Enter target(s): scanme.nmap.org 192.168.1.1

MAIN MENU - PwnScanner

[1] Host Discovery

[2] Port Scanning

[3] Service Discovery

[4] OS Discovery

[5] Firewall Evasion / Bypass

[6] Run ALL with Aggressive (-A -T4)

[0] Exit

[?] Select option [0-6]: 2

**PORT SCANNING - PwnScanner**

[1] SYN Stealth Scan

[2] TCP Connect Scan

[10] Scan all 65535 ports

[11] Scan top 100 ports

[0] Back to main menu


[?] Select option [0-14]: 1


**File Structure**

PwnScanner.py         # Main script (single file, no dependencies)

targets.txt           # Optional: target list file

PwnScanner_scan_*.txt # Saved scan results (auto-generated)

Output / Results

Scan results are streamed in real-time to the terminal with full Nmap output. Optionally, results can be saved to timestamped text files with the following structure:


# Author: PwnPilot

GitHub: github.com/PwnPilot
