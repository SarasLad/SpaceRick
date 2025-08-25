import socket
import whois
import dns.resolver

def format_date(value):
    if isinstance(value, list):
        return value[0].strftime("%Y-%m-%d") if value else "N/A"
    elif hasattr(value, "strftime"):
        return value.strftime("%Y-%m-%d")
    return str(value)

def get_dns_info(domain):
    print(f"\n🌐 [DNS Info] Gathering DNS data for: {domain}")
    try:
        ip = socket.gethostbyname(domain)
        print(f"  [✔] Resolved IP: {ip}")
    except Exception as e:
        print(f"  [!] IP Resolution failed: {e}")

    try:
        ns_records = dns.resolver.resolve(domain, 'NS')
        print("  [✔] Nameservers:")
        for ns in ns_records:
            print(f"      - {ns.to_text()}")
    except:
        print("  [!] No NS records found.")

    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        print("  [✔] Mail Servers:")
        for mx in mx_records:
            print(f"      - {mx.exchange} (Priority {mx.preference})")
    except:
        print("  [!] No MX records found.")

def get_whois_info(domain):
    print(f"\n📜 [WHOIS Info] Fetching registrar details for: {domain}")

    try:
        w = whois.whois(domain)
        print(f"  [✔] Registrar: {w.registrar}")
        print(f"  [✔] Creation Date: {format_date(w.creation_date)}")
        print(f"  [✔] Expiry Date: {format_date(w.expiration_date)}")
        print(f"  [✔] Country: {w.country}")
        print(f"  [✔] Domain Name: {w.domain_name}")
    except Exception as e:
        print(f"  [!] WHOIS lookup failed: {e}")
