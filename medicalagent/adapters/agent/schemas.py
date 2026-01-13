from typing import Any

from pydantic import BaseModel


class AgentContext(BaseModel):
    container: Any
    dialog_id: int
