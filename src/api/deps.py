from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.session import get_async_session


db_d = Annotated[AsyncSession, Depends(get_async_session)]