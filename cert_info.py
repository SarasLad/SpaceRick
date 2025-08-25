import ssl
import socket
from urllib.parse import urlparse
from datetime import datetime

def flatten_name(name):
    return {k: v for tup in name for (k, v) in tup}

def get_certificate_info(url):
    print(f"[🔐] Fetching certificate info for: {url}")

    parsed_url = urlparse(url)
    hostname = parsed_url.netloc or parsed_url.path  # fallback for URLs without scheme
    port = 443

    context = ssl.create_default_context()

    try:
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

                print("\n📜 Certificate Info:")
                print(f"  Subject: {flatten_name(cert['subject'])}")
                print(f"  Issuer: {flatten_name(cert['issuer'])}")
                print(f"  Serial Number: {cert.get('serialNumber')}")
                print(f"  Signature Algorithm: {cert.get('signatureAlgorithm', 'N/A')}")
                print(f"  Valid From: {cert['notBefore']}")
                print(f"  Valid To:   {cert['notAfter']}")

                # Expiration check
                expiry = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                remaining = expiry - datetime.utcnow()
                print(f"  Expires in: {remaining.days} day(s)")

                # Subject Alternative Names
                san = cert.get("subjectAltName")
                if san:
                    print(f"  Subject Alt Names:")
                    for typ, name in san:
                        print(f"    → {typ}: {name}")
    except Exception as e:
        print(f"[!] Failed to retrieve certificate info: {e}")
