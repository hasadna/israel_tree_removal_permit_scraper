import typing
from pathlib import Path


def parse_status(stem: str):
    stem = stem.lower()
    if "befor" in stem:
        return "before"
    if "after" in stem:
        return "after"
    if "aftar" in stem:
        return "after"
    assert False, f"Can't parse: {stem!r}"


def parse_region(stem: str):
    stem = stem.lower()
    for s in [
        "trees",
        "tree",
        "before",
        "befor",
        "after",
        "aftar",
    ]:
        stem = stem.replace(s, "")
    stem = stem.strip("_").replace("_", "-")
    return stem or "general"


class DocUrl(typing.NamedTuple):
    region: str
    status: str
    extension: str
    url: str

    @property
    def filename(self):
        return f"{self.region}-{self.status}{self.extension}"


def parse_urls(urls):
    for url in urls:
        p = Path(url)
        yield DocUrl(
            parse_region(p.stem),
            parse_status(p.stem),
            p.suffix.lower(),
            url,
        )
