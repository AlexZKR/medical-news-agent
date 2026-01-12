from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from medicalagent.drivers.di import DIContainer


class AgentContext(BaseModel):
    container: DIContainer
    dialog_id: int
