from fastapi import APIRouter, Request

from trawl.core.schema import CompanyUrlInput
from trawl.discovery.dedupe import deduplicate_links
from trawl.discovery.filter_links import filter_links
from trawl.discovery.scoring import score_links
from trawl.fetcher.extractor import page_fetcher
from trawl.fetcher.schema import PageFetchResult

router = APIRouter()


@router.post("/")
async def fetch_page(request: Request, url: CompanyUrlInput):
    browser = request.app.state.browser
    result = await page_fetcher(browser, url)
    filtered = filter_links(result.data)
    deduped = deduplicate_links(filtered)
    scores = score_links(deduped)
    return scores
