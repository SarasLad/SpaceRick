import requests
from urllib.parse import urljoin
import os

DEFAULT_WORDLIST = [
    "admin", "login", "dashboard", "config", ".git", "backup",
    "uploads", "files", "data", "private", "server-status"
]

def load_wordlist(path=None):
    if not path:
        return DEFAULT_WORDLIST
    if not os.path.isfile(path):
        print(f"[!] Wordlist file '{path}' not found. Using default wordlist.")
        return DEFAULT_WORDLIST
    try:
        with open(path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[!] Failed to load wordlist '{path}': {e}")
        print("[*] Falling back to default wordlist.")
        return DEFAULT_WORDLIST

def bruteforce_dirs(base_url, wordlist_path=None):
    found = []
    wordlist = load_wordlist(wordlist_path)

    print(f"[🔍] Starting directory bruteforce on {base_url} with {len(wordlist)} entries.")

    for dir_name in wordlist:
        url = urljoin(base_url, dir_name + "/")
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                # Direct success
                print(f"  [⚠️] Found: {url} → 200 OK")
                found.append((url, 200))
            elif response.status_code in [301, 302, 307]:
                location = response.headers.get("Location", "")
                # If redirect is to exact same path (e.g., just adding slash), ignore
                if not location.endswith(dir_name + "/"):
                    print(f"  [⚠️] Redirected: {url} → {location} (Status: {response.status_code})")
                    found.append((url, response.status_code))
                else:
                    print(f"  [➖] Trivial redirect at {url}")
            elif response.status_code == 403:
                print(f"  [🚫] Forbidden (403): {url}")
                found.append((url, 403))
            else:
                print(f"  [✖] {url} → {response.status_code}")

        except requests.RequestException as e:
            print(f"  [!] Error with {url}: {e}")

    return found
