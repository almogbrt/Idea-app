from __future__ import annotations

from pydantic import BaseModel


class EmailView(BaseModel):
    id: str
    sender: str
    subject: str
    snippet: str
    date: str
