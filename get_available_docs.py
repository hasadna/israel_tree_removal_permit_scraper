from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

URL = "https://www.moag.gov.il/yhidotmisrad/forest_commissioner/rishyonot_krita/Pages/default.aspx"


def extract_docs(html):
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a"):
        url = a.get("href") or ""
        if "Documents" in url and "xls" in url.lower():
            yield url


r = requests.get(URL)
r.raise_for_status()
urls = {urljoin(URL, url) for url in extract_docs(r.content)}

with open("doc_urls.txt", "w") as f:
    f.write("\n".join(sorted(urls)))
