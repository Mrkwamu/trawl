class TrawlError(Exception):
    code = "TRAWL_ERROR"
    message = "Something went wrong"
    status_code = 500


class PageTimeoutError(TrawlError):
    code = "PAGE_TIMEOUT"
    message = "The page took too long to load"
    status_code = 504


class DomainNotFoundError(TrawlError):
    code = "DOMAIN_NOT_FOUND"
    message = "This domain could not be found"
    status_code = 422


class BadStatusError(TrawlError):
    code = "BAD_STATUS"
    message = "The site replied with an error status"
    status_code = 502

class PageNotFoundError(TrawlError):
    code = "PAGE_NOT_FOUND"
    message = "This page could not be found"
    status_code = 404

class FetchFailedError(TrawlError):
    code = "FETCH_FAILED"
    message = "Could not fetch the page"
    status_code = 502

class SiteBlockedError(TrawlError):
    code = "SITE_BLOCKED"
    message = "The site refused our request, it may block automated access"
    status_code = 502