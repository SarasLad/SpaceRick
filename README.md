# 🔎 SpaceRick

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)


A **modular web scanner** built as a lightweight CLI tool.  
SpaceRick helps penetration testers and bug bounty hunters quickly identify common web vulnerabilities with a simple command-line interface.

---

## ✨ Features
- 🔥 **XSS Detection** – Test for cross-site scripting vulnerabilities  
- 💉 **SQL Injection Detection** – Check for injectable parameters  
- 📂 **Directory Bruteforce** – Discover hidden files & directories  
- 🔐 **SSL/TLS Info** – Fetch certificate details for HTTPS endpoints  
- 🌐 **DNS & WHOIS Lookup** – Gather domain intelligence  

---

## 📦 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/SarasLad/SpaceRick.git
cd webscanner
pip install -e .
```

## Usage

```bash
  base: |
    spacerick <target> [options]
  example: |
    spacerick https://example.com --xss --sqli --dns
  options:
    - flag: "--xss"
      description: "Run XSS scan"
    - flag: "--sqli"
      description: "Run SQL Injection scan"
    - flag: "--bruteforce"
      description: "Run directory bruteforce"
    - flag: "--cert"
      description: "Get SSL/TLS certificate info"
    - flag: "--dns"
      description: "Run DNS & WHOIS lookup"
```

## Features 
  - Detect Cross-Site Scripting (XSS) vulnerabilities
  - Scan for SQL Injection flaws
  - Perform directory bruteforce to find hidden paths
  - Retrieve SSL/TLS certificate details
  - Run DNS & WHOIS lookups
  - Modular design for easy feature expansion

## License
  MIT License © 2025 Saras Lad
