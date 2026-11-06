from urllib.parse import urlparse

import tldextract

from trawl.discovery.constants import (
    ATS_DOMAINS,
    CAREER_KEYWORDS,
    CAREER_PATHS,
    MAX_CANDIDATES,
    SCORE_THRESHOLD,
    TRAWL_SCORE,
)
from trawl.discovery.text import clean_path_piece, clean_text


def score_links(items: list[dict[str, str]]):
    scored_links = []

    for item in items:
        text = clean_text(item.get("text", ""))
        href = item.get("href", "")

        ext = tldextract.extract(href)
        domain = f"{ext.domain}.{ext.suffix}"
        path_pieces = [
            clean_path_piece(piece) for piece in urlparse(href).path.split("/")
        ]

        score = 0
        clues = []

        if domain in ATS_DOMAINS:
            score += TRAWL_SCORE["ATS_SCORE"]
            clues.append("ats")

        if any(piece in CAREER_PATHS for piece in path_pieces):
            score += TRAWL_SCORE["PATH_SCORE"]
            clues.append("path")

        if text in CAREER_KEYWORDS:
            score += TRAWL_SCORE["TEXT_SCORE"]
            clues.append("text")

        if score >= SCORE_THRESHOLD:
            scored_links.append(
                {"text": text, "href": href, "score": score, "clues": clues}
            )

    scored_links.sort(key=lambda link: link["score"], reverse=True)

    return scored_links[:MAX_CANDIDATES]
