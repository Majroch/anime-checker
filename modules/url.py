from urllib.parse import urlparse

links = (
    ("cda.pl", "Cda"),
    ("4anime.one", "ForAnimeDotOne"),
    ("wbijam.pl", "Wbijam"),
)

def identifyUrl(url: str) -> str:
    parsed = urlparse(url)
    for link in links:
        if link[0] in parsed.netloc:
            return link[1]
    return ""
