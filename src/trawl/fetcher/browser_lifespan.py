import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)

@asynccontextmanager
async def browser_lifespan(app: FastAPI):
    logger.info("Starting Playwright and launching browser")

    async with async_playwright() as playwright:
        try:
            browser = await playwright.chromium.launch(
                channel="chrome",
                headless=True,
            )
        except Exception:
            logger.exception("Failed to launch browser")
            raise

        app.state.browser = browser
        logger.info("Browser ready")

        try:
            yield
        finally:
            logger.info("Closing browser")
            await browser.close()
            logger.info("Browser closed")