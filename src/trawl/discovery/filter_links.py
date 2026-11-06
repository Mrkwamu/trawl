from urllib.parse import urlparse

from trawl.discovery.constants import NEGATIVE_DOMAINS, NEGATIVE_KEYWORDS
from trawl.discovery.schema import FilterLinkResult
from trawl.discovery.text import clean_text


def filter_links(items: list[dict[str, str]]) -> FilterLinkResult:
    filtered_link = []

    for item in items:
        text = item.get("text", "")
        href = item.get("href", "")

        text = clean_text(text)
        hostname = urlparse(href).hostname

        if href.startswith(("mailto:", "tel:", "sms:", "javascript:")):
            continue

        if any(keywords in text for keywords in NEGATIVE_KEYWORDS):
            continue

        if hostname:
            hostname = hostname.removeprefix("www.")

            if any(
                hostname == domain or hostname.endswith(f".{domain}")
                for domain in NEGATIVE_DOMAINS
            ):
                continue

        filtered_link.append(
            {
                "text": text,
                "href": href,
            }
        )

    return filtered_link
