import socket
import http.client
import requests
import re
from urllib.parse import urlparse, urljoin
from scanner import xss
from scanner import sqli
from scanner import bruteforce
from scanner import cert_info
from scanner import dns_whois

def scan_ports(host, ports=None):
    if ports is None:
        ports = [21, 22, 80, 443, 3306]
    open_ports = []
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex((host, port))
                if result == 0:
                    open_ports.append(port)
        except Exception:
            pass
    return open_ports

def check_headers(url):
    required_headers = [
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Content-Security-Policy"
    ]
    try:
        response = requests.head(url, timeout=5)
        headers = response.headers
        missing = [h for h in required_headers if h not in headers]
        return missing
    except Exception as e:
        print(f"[!] Header check failed: {e}")
        return required_headers

def crawl_links(url, max_links=5):
    links = set()
    try:
        response = requests.get(url, timeout=5)
        hrefs = re.findall(r'href=["\'](.*?)["\']', response.text)
        for href in hrefs:
            full_url = urljoin(url, href)
            links.add(full_url)
    except Exception as e:
        print(f"[!] Error crawling: {e}")
    return list(links)[:max_links]

def run_xss(url):
    print("[*] Running XSS scanner...")
    xss.scan_xss(url)

def run_sqli(url):
    print("[*] Running SQL Injection scanner...")
    sqli.scan_sqli(url)

def run_bruteforce(url):
    print("[*] Running Directory Bruteforce...")
    bruteforce.bruteforce_dirs(url)

def run_cert_info(url):
    print("[*] Fetching SSL Certificate Info...")
    cert_info.fetch_cert_info(url)

def run_dns_whois(url):
    print("[*] Running DNS and WHOIS Lookup...")
    dns_whois.dns_lookup(url)
    dns_whois.whois_lookup(url)
