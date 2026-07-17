from __future__ import annotations

import uuid

from pydantic import BaseModel


class CurrentUserResponse(BaseModel):
    id: uuid.UUID
    email: str
    name: str
