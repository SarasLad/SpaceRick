import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_forms(url):
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        return soup.find_all("form")
    except Exception as e:
        print(f"[!] Error fetching forms: {e}")
        return []

def extract_form_details(form, base_url):
    details = {
        "action": "",
        "method": "get",
        "fields": []
    }

    action = form.attrs.get("action")
    method = form.attrs.get("method", "get").lower()
    input_tags = form.find_all("input")

    details["action"] = urljoin(base_url, action) if action else base_url
    details["method"] = method

    for field_tag in input_tags:
        field_type = field_tag.attrs.get("type", "text")
        field_name = field_tag.attrs.get("name")
        details["fields"].append({"type": field_type, "name": field_name})

    return details
