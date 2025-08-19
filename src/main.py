from argparse import ArgumentParser
from contextlib import asynccontextmanager
from os import cpu_count, environ, getenv
from platform import system

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware
from uvicorn import run

from .api import api_router
from .core.config import settings
from .core.db.init_db import initialize_db
from .core.db.session import async_engine
from .core.utils.custom_logging import setup_logging


def is_debug_mode() -> bool:
    return getenv("APP_DEBUG", "0") == "1"


@asynccontextmanager
async def lifespan(_: FastAPI):
    if is_debug_mode():
        await initialize_db()
    yield
    await async_engine.dispose()


def create_application() -> FastAPI:
    """Factory function to create FastAPI application."""
    app = FastAPI(**settings.f_api.model_dump(), lifespan=lifespan,
                  default_response_class=ORJSONResponse)
    app.add_middleware(
        CORSMiddleware,
        **settings.cors.model_dump()  # type: ignore
    )
    app.include_router(api_router)

    return app


def main() -> None:
    """Main application entry point."""
    parser = ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    environ["APP_DEBUG"] = f"{int(args.debug)}"

    setup_logging(args.debug)

    run(
        'src.main:create_application',
        host=args.host,
        port=args.port,
        reload=args.debug,
        workers=max((cpu_count() or 2) - 1, 1) if not args.debug else 1,
        loop="asyncio" if system().lower() == "windows" else "uvloop",
        factory=True
    )


if __name__ == '__main__':
    main()
