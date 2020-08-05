from urllib.parse import urlparse

links = (
    ("cda.pl", "Cda"),
    ("4anime.one", "ForAnimeDotOne"),
)

def identifyUrl(url: str) -> str:
    parsed = urlparse(url)
    for link in links:
        if parsed.netloc == link[0] or parsed.netloc == "www." + link[0]:
            return link[1]
    return ""
