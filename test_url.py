from trawl.core.urls import normalize_url


TEST_URLS = [
    # Valid URLs
    "stripe.com",
    "https://stripe.com",
    "http://stripe.com",
    "www.stripe.com",
    "\twww.stripe.com",
    "STRIPE.COM",
    "stripe.com/careers",
    "https://stripe.com/jobs",
    "https://jobs.lever.co/figma",
    "https://boards.greenhouse.io/figma",
    "https://example.com/careers?page=2",
    "  stripe.com  ",
    "https://sub.example.com/jobs",

    # Invalid URLs
    "",
    "   ",
    "not-a-website",
    "stripe",
    "https://",
    "https://.com",
    "https://stripe..com",
    "ftp://stripe.com",
    "javascript:alert(1)",
    "https://stripe.com:abc",
    "https://user:pass@stripe.com",

    # Unsafe URLs
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://192.168.1.1",
    "http://10.0.0.5",
    "http://172.16.0.1",
    "http://169.254.169.254",
    "http://[::1]",

    # Edge cases
    "https://example.com:443/careers",
    "HTTPS://EXAMPLE.COM/Jobs",
    "https://example.com/#careers",
    "https://example.com@127.0.0.1/",
    "https://127.0.0.1@example.com/",
    "https://example.com./careers",
    "https://example.com/%ZZ",
]

for url in TEST_URLS:
    try:
        result = normalize_url(url)
        print(f"PASS | {url!r} -> {result}")

    except Exception as exc:
        print(f"REJECTED | {url!r}")