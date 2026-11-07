from urllib.parse import parse_qsl, urlencode, urlparse

TRACKING_PARAMS = {"fbclid", "gclid"}
TRACKING_PREFIXES = ("utm_",)


def make_link_key(href: str) -> str:
    href = href.strip()
    parsed = urlparse(href)

    host = parsed.hostname
    if not host:
        return href

    host = host.removeprefix("www.")
    path = parsed.path.rstrip("/")

    query = [
        (name, value)
        for name, value in parse_qsl(parsed.query, keep_blank_values=True)
        if name.lower() not in TRACKING_PARAMS
        and not name.lower().startswith(TRACKING_PREFIXES)
    ]
    query.sort()

    return f"{host}{path}?{urlencode(query)}"


def deduplicate_links(items: list[dict[str, str]]) -> list[dict[str, str]]:
    kept: dict[str, dict[str, str]] = {}

    for item in items:
        key = make_link_key(item.get("href", ""))

        if key not in kept:
            kept[key] = item
        elif not kept[key].get("text", "").strip() and item.get("text", "").strip():
            kept[key] = (
                item  
            )

    return list(kept.values())
