"""schema"""
from typing import Optional

from pydantic import BaseModel


class InfoResponse(BaseModel):
    """info response"""

    oktaDomain: Optional[str]
    oktaClientId: Optional[str]
