from pydantic import BaseModel


class PageFetchResult(BaseModel):
    final_url: str
    data: list[dict[str, str]] | None = None
