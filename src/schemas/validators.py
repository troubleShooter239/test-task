from typing import Annotated

from pydantic import EmailStr, Field, SecretStr

Email = Annotated[EmailStr, Field(max_length=50)]
Password = Annotated[SecretStr, Field(max_length=16)]

StrName = Annotated[str, Field(max_length=32)]
Str255 = Annotated[str, Field(max_length=255)]
