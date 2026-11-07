from playwright.async_api import Browser, TimeoutError
from playwright.async_api import Error as playwright_Error

from trawl.core.errors import (
    BadStatusError,
    DomainNotFoundError,
    FetchFailedError,
    PageTimeoutError,
    SiteBlockedError,
)
from trawl.core.schema import CompanyUrlInput
from trawl.fetcher.schema import PageFetchResult


async def page_fetcher(
    browser: Browser, companyUrl: CompanyUrlInput
) -> PageFetchResult:
    user_agent = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        f"Chrome/{browser.version} Safari/537.36"
    )
    context = await browser.new_context(user_agent=user_agent)
    try:
        page = await context.new_page()
        response = await page.goto(str(companyUrl.url))

        if response is None:
            raise FetchFailedError()

        if response.status in (403, 409):
            raise SiteBlockedError()

        if not response.ok:
            raise BadStatusError

        locator = page.locator("a[href], iframe[src]")

        links = await locator.evaluate_all("""
                                           elements => elements.map(el => ({
                                               text: el.innerText?.trim() || "",
                                               href: el.href || el.src
                                           }))
                                           """)

        return PageFetchResult(
            final_url=response.url,
            data=links,
        )

    except TimeoutError as e:
        raise PageTimeoutError() from e

    except playwright_Error as e:
        if "ERR_NAME_NOT_RESOLVED" in str(e):
            raise DomainNotFoundError() from e

        raise FetchFailedError() from e

    finally:
        await context.close()
