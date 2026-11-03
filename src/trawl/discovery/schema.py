from pydantic import BaseModel


class FilterLinkResult(BaseModel):
    filter_links: list[dict[str, str]]
