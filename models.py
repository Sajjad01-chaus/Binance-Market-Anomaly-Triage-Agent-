from pydantic import BaseModel, Field
from typing import Literal

class MarketEvent(BaseModel):
    symbol: str
    event_type: str
    price_change_percent: float
    volume_surge: float
    context: str

class AgentDecision(BaseModel):
    relevance_score: float = Field(..., description="Score from 0.0 to 1.0 representing signal importance")
    priority: Literal["LOW", "MEDIUM", "HIGH"]
    action: Literal["IGNORE", "ALERT_ANALYST", "EXECUTE_TRADE"]
    reasoning: str = Field(..., description="One sentence explaining the priority reasoning")