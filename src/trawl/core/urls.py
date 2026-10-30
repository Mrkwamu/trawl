


from pydantic import ValidationError

from trawl.core.schema import CompanyUrlInput


def normalize_url(raw_url: str) -> str:
    try:
        validated_url = CompanyUrlInput(url=raw_url).url
        return str(validated_url)

    except ValidationError as exc:
        error_type = exc.errors()[0]["type"]

        if error_type == "url_scheme":
            raise ValueError("Only HTTP and HTTPS URLs are supported") from exc

        if error_type == "url_parsing":
            raise ValueError("Invalid URL format") from exc

        raise