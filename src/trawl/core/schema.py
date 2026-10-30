import re

from pydantic import BaseModel, HttpUrl, field_validator
from tldextract import tldextract

HOSTNAME_LABEL_PATTERN = re.compile(r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?")

class CompanyUrlInput(BaseModel):
    url: HttpUrl

    @field_validator('url', mode='before')
    @classmethod
    def prepare_url(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError('Url must be a string')

        cleaned_url = value.strip()

        if not cleaned_url:
            raise ValueError('Url must not be empty')

        if '://' not in cleaned_url:
            cleaned_url = f"https://{cleaned_url}"

        return cleaned_url


    @field_validator('url', mode='after')
    @classmethod
    def validate_url(cls, url: HttpUrl) -> HttpUrl:
        hostname = url.host

        if not hostname:
            raise ValueError("URL must contain a hostname")

        if url.username is not None or url.password is not None:
            raise ValueError("URL credentials are not allowed")

        labels = hostname.rstrip(".").split(".")

        if hostname.endswith(".") or not all(
                HOSTNAME_LABEL_PATTERN.fullmatch(label) for label in labels
        ):
            raise ValueError("Invalid hostname format")

        extracted_domain = tldextract.extract(hostname)

        if not extracted_domain.domain or not extracted_domain.suffix:
            raise ValueError("URL must contain a recognized public domain suffix")

        return url

