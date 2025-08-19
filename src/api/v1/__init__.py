from fastapi import APIRouter

from . import tasks


v1_router = APIRouter(prefix='/v1')
v1_router.include_router(tasks.router)


@v1_router.get("/ping")
async def ping() -> dict[str, str]:
    """
    Health-check endpoint.

    Returns:
        dict[str, str]: Simple JSON with "pong" message.
    """
    return {"message": "pong"}
