import argparse
import pyfiglet
from rich.console import Console
from scanner import core

console = Console()

def print_banner():
    ascii_banner = pyfiglet.figlet_format("SpaceRick", font="slant")
    console.print(ascii_banner, style="bold green")
    console.print("[bold cyan] Modular Web Scanner[/]\n")

def main():
    print_banner()

    parser = argparse.ArgumentParser(
        prog="SpaceRick",
        description = "A modular web Vulnerability scanner CLI tool"
    )

    parser.add_argument("url", help="Target URL")
    parser.add_argument("--xss", action="store_true", help="Run XSS test")
    parser.add_argument("--sqli", action="store_true", help="Run SQL Injection test")
    parser.add_argument("--dir", action="store_true", help="Run Directory Bruteforce")
    parser.add_argument("--cert", action="store_true", help="Get SSL Certificate Info")
    parser.add_argument("--dns", action="store_true", help="Run DNS/WHOIS Recon")

    args = parser.parse_args()

    if args.xss:
        core.run_xss(args.url)
    if args.sqli:
        core.run_sqli(args.url)
    if args.dir:
        core.run_bruteforce(args.url)
    if args.cert:
        core.run_cert_info(args.url)
    if args.dns:
        core.run_dns_whois(args.url)

if __name__ == "__main__":
    main()
