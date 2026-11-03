import logging

from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from trawl.core.errors import TrawlError
from trawl.fetcher.browser_lifespan import browser_lifespan
from trawl.fetcher.routes import router

app = FastAPI(lifespan=browser_lifespan)

@app.exception_handler(TrawlError)
async def trawl_error_handler(request: Request, exc: TrawlError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.code,
            "message": exc.message,
        }
    )
app.include_router(router)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

