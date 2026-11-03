from fastapi import APIRouter, Request

from trawl.core.schema import CompanyUrlInput
from trawl.fetcher.extractor import page_fetcher
from trawl.fetcher.schema import PageFetchResult

router = APIRouter()

@router.post("/", response_model=PageFetchResult)
async def fetch_page(request: Request, url: CompanyUrlInput):
    browser = request.app.state.browser
    return await page_fetcher(browser, url )