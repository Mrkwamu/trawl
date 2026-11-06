from urllib.parse import urlparse

import tldextract

from trawl.discovery.constants import NEGATIVE_DOMAINS, NEGATIVE_KEYWORDS
from trawl.discovery.schema import FilterLinkResult
from trawl.discovery.text import clean_text


def filter_links(domain: str, items: list[dict[str, str]]) -> FilterLinkResult:
    filtered_link = []
    ext = tldextract.extract(domain)
    company_domain = f"{ext.domain}.{ext.suffix}"
    blocked_domains = NEGATIVE_DOMAINS.copy()

    blocked_domains.discard(company_domain)

    for item in items:
        text = clean_text(item.get("text", ""))
        href = item.get("href", "")

        parsed = urlparse(href)
        hostname = parsed.hostname

        if href.startswith(("mailto:", "tel:", "sms:", "javascript:")):
            continue

        if any(keywords in text for keywords in NEGATIVE_KEYWORDS):
            continue

        if hostname:
            hostname = hostname.removeprefix("www.")

            if any(
                hostname == blocked_domain or hostname.endswith(f".{blocked_domain}")
                for blocked_domain in blocked_domains
            ):
                continue

        filtered_link.append(
            {
                "text": text,
                "href": href,
            }
        )

    return filtered_link
