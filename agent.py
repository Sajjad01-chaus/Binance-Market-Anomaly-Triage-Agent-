import json
from groq import Groq
from pydantic import ValidationError
from config import GROQ_API_KEY, MODEL_NAME
from models import MarketEvent, AgentDecision

client = Groq(api_key=GROQ_API_KEY)

def triage_market_event(event: MarketEvent) -> AgentDecision:
    prompt = f"""
    You are an elite quantitative trading FDE. Analyze this market event and output a JSON decision.
    
    Event Data:
    Symbol: {event.symbol}
    Type: {event.event_type}
    Price Change: {event.price_change_percent}%
    Volume Surge: {event.volume_surge}x
    Context: {event.context}
    
    Triage Logic:
    - IGNORE (LOW Priority): Minor fluctuations or volume spikes with neutral/normal context. The goal is strict noise reduction.
    - ALERT_ANALYST (MEDIUM Priority): Abnormal volume or price movement driven by macro news, requiring human review before action.
    - EXECUTE_TRADE (HIGH Priority): Price drop > 5% AND severe negative context (e.g., hack, delisting, exploit) OR massive volume surge > 5x indicating immediate institutional dumping.
    
    Respond STRICTLY with JSON matching this schema:
    {{
        "relevance_score": float,
        "priority": "LOW" | "MEDIUM" | "HIGH",
        "action": "IGNORE" | "ALERT_ANALYST" | "EXECUTE_TRADE",
        "reasoning": "string"
    }}
    """

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        
        raw_json = json.loads(response.choices[0].message.content)
        decision = AgentDecision(**raw_json)
        return decision

    except (ValidationError, json.JSONDecodeError) as e:
        return AgentDecision(
            relevance_score=0.0,
            priority="LOW",
            action="IGNORE",
            reasoning=f"Pipeline error or LLM hallucination: {str(e)}"
        )