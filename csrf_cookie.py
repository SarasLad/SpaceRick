import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def check_cookie_security(url):
    print(f"\n🍪 [Cookie Security] Checking cookies on: {url}")
    try:
        res = requests.get(url)
        cookies = res.cookies

        if not cookies:
            print("  [–] No cookies set by the server.")
            return

        for cookie in res.cookies:
            print(f"  [🍪] Cookie: {cookie.name}")
            print(f"      - Secure: {'✅' if cookie.secure else '❌'}")
            print(f"      - HttpOnly: {'✅' if 'httponly' in cookie._rest else '❌'}")
            print(f"      - SameSite: {cookie._rest.get('samesite', '❌')}")
    except Exception as e:
        print(f"  [!] Cookie check failed: {e}")

def check_csrf_tokens(url):
    print(f"\n🛡️ [CSRF Check] Looking for CSRF protections on: {url}")
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        forms = soup.find_all("form")

        if not forms:
            print("  [–] No forms found on this page.")
            return

        for i, form in enumerate(forms, 1):
            has_token = False
            for input_tag in form.find_all("input"):
                name = input_tag.get("name", "").lower()
                if "csrf" in name or "token" in name:
                    has_token = True
                    break
            action = form.get("action", "[no action]")
            method = form.get("method", "get").upper()

            print(f"  [🧾] Form {i}: Method={method}, Action={action}")
            if method == "POST" and not has_token:
                print("      ⚠️ No CSRF token detected!")
            elif has_token:
                print("      ✅ CSRF token found.")
    except Exception as e:
        print(f"  [!] CSRF check failed: {e}")
