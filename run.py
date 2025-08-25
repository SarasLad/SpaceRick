from scanner.core import scan_ports, check_headers, crawl_links
from urllib.parse import urlparse
from scanner.forms import get_forms, extract_form_details
from scanner.xss import test_xss
from scanner.sqli import test_sqli
from scanner.bruteforce import bruteforce_dirs
from scanner.cert_info import get_certificate_info
from scanner.csrf_cookie import check_cookie_security, check_csrf_tokens
from scanner.dns_whois import get_dns_info, get_whois_info

def main():
    url = input("Enter the target URL (e.g., https://example.com): ").strip()
    parsed = urlparse(url)
    host = parsed.hostname

    print(f"\n== Scanning: {url} ==\n")

    print("[1] Crawling links...")
    links = crawl_links(url)
    for link in links:
        print(f"  ➤ {link}")

    print("\n[2] Scanning ports...")
    ports = scan_ports(host)
    print(f"  Open Ports: {ports if ports else 'None found'}")

    print("\n[3] Checking security headers...")
    missing = check_headers(url)
    print(f"  Missing Headers: {missing if missing else 'All present'}")

    print("\n[4] Detecting forms...")
    forms = get_forms(url)
    if forms:
        for i, form in enumerate(forms, 1):
            form_details = extract_form_details(form, url)
            print(f"\n  [Form {i}]")
            print(f"    Action : {form_details['action']}")
            print(f"    Method : {form_details['method']}")
            print(f"    Fields :")
            for field in form_details['fields']:
                print(f"      - {field['name']} ({field['type']})")
    print("\n== Scan Complete ✅ ==")

    print("\nWhat would you like to perform next?")
    print("1. XSS Injection")
    print("2. SQL Injection")
    print("3. Directory Bruteforce")
    print("4. Certificate Information")
    print("5. Cookie and CSRF Check")
    print("6. DNS WHOIS Lookup")
    print("7. Perform All")

    choice = input("Enter the number(s) separated by comma (e.g., 1,3): ").strip()
    choices = [c.strip() for c in choice.split(",")]

    if '1' in choices or '7' in choices:
        print("\n[🔥] Running XSS Injection test...")
        vulns = test_xss(url)
        if vulns:
            print(f"\n[!] XSS Vulnerabilities found in {len(vulns)} form(s).")
            for target_url, data, payload in vulns:
                print(f"\n  [!] Vulnerable URL: {target_url}")
                print(f"      Payload Used: {payload}")
        else:
            print("\n[✔] No XSS vulnerabilities detected.")

    if '2' in choices or '7' in choices:
        print("\n[🧨] Running SQL Injection test...")
        sqli_vulns = test_sqli(url)
        if sqli_vulns:
            print(f"\n[!] SQL Injection vulnerabilities found in {len(sqli_vulns)} form(s):")
            for target_url, data, payload in sqli_vulns:
                print(f"  → {target_url} | Payload: {payload}")
        else:
            print("[✔] No SQLi vulnerabilities detected.")

    if '3' in choices or '7' in choices:
        print("\n[🔎] Running Directory Bruteforce...")

        use_custom = input("Do you want to use a custom wordlist? (y/n): ").strip().lower()
        wordlist_path = None

        if use_custom == 'y':
            wordlist_path = input("Enter path to your wordlist file: ").strip()
            if not wordlist_path:
                print("[!] No path entered. Using default wordlist.")
                wordlist_path = None  # fallback to default
        else:
            print("[*] Using default wordlist.")

        print(f"[*] Starting scan using: {wordlist_path or 'default wordlist'}")

        try:
            dirs_found = bruteforce_dirs(url, wordlist_path)
        except Exception as e:
            print(f"[!] Bruteforce failed due to: {e}")
            dirs_found = []

        if dirs_found:
            print(f"\n[!] Found {len(dirs_found)} potential directories:")
            for d_url, code in dirs_found:
                print(f"  → {d_url} (Status: {code})")
        else:
            print("[✔] No interesting directories found.")

    if '4' in choices or '7' in choices:
        print("\n[🔍] Retrieving TLS Certificate Info...")
        get_certificate_info(url)

    if '5' in choices or '7' in choices:
        check_cookie_security(url)
        check_csrf_tokens(url)

    if '6' in choices or '7' in choices:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path
        get_dns_info(domain)
        get_whois_info(domain)



if __name__ == "__main__":
    main()
