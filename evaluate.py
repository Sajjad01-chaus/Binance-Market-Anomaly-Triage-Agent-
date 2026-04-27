import time
from agent import triage_market_event
from models import MarketEvent

# Expanded dataset to test Noise Reduction
DATASET = [
    {"event": MarketEvent(symbol="BTC", event_type="PRICE_DROP", price_change_percent=-8.5, volume_surge=6.2, context="Major exchange hack reported."), "expected_action": "EXECUTE_TRADE"},
    {"event": MarketEvent(symbol="ETH", event_type="FLUCTUATION", price_change_percent=0.5, volume_surge=1.1, context="Normal market hours."), "expected_action": "IGNORE"},
    {"event": MarketEvent(symbol="SOL", event_type="NEWS", price_change_percent=2.0, volume_surge=3.0, context="New protocol upgrade announced."), "expected_action": "ALERT_ANALYST"},
    {"event": MarketEvent(symbol="DOGE", event_type="SOCIAL_MENTION", price_change_percent=1.2, volume_surge=4.0, context="Celebrity tweeted a meme."), "expected_action": "IGNORE"},
    {"event": MarketEvent(symbol="USDC", event_type="DEPEG_WARNING", price_change_percent=-3.0, volume_surge=8.0, context="Unconfirmed rumors of reserve shortages."), "expected_action": "EXECUTE_TRADE"},
    {"event": MarketEvent(symbol="ADA", event_type="FLUCTUATION", price_change_percent=-0.2, volume_surge=0.9, context="Routine low volatility."), "expected_action": "IGNORE"}
]

def calculate_score():
    print("Running FDE Evaluation Pipeline...\n")
    correct_actions = 0
    total_latency = 0
    
    # Metrics for Noise Reduction
    expected_ignores = 0
    correct_ignores = 0
    
    for item in DATASET:
        if item["expected_action"] == "IGNORE":
            expected_ignores += 1
            
        start_time = time.time()
        decision = triage_market_event(item["event"])
        latency = time.time() - start_time
        total_latency += latency
        
        is_correct = decision.action == item["expected_action"]
        if is_correct:
            correct_actions += 1
            if decision.action == "IGNORE":
                correct_ignores += 1
            
        print(f"Event: {item['event'].symbol} | Expected: {item['expected_action']} | Got: {decision.action} | Time: {latency:.2f}s")

    # Core Metrics
    accuracy = correct_actions / len(DATASET)
    avg_latency = total_latency / len(DATASET)
    noise_reduction_rate = correct_ignores / expected_ignores if expected_ignores > 0 else 1.0
    
    # The New 10,000 Point Formula: 60% Accuracy, 20% Latency, 20% Noise Reduction
    accuracy_score = accuracy * 6000
    latency_score = max(0, 2000 - (avg_latency * 1000)) 
    noise_reduction_score = noise_reduction_rate * 2000
    
    final_score = int(accuracy_score + latency_score + noise_reduction_score)
    
    print("-" * 30)
    print(f"Accuracy: {accuracy * 100:.1f}%")
    print(f"Noise Reduction Rate: {noise_reduction_rate * 100:.1f}%")
    print(f"Avg Latency: {avg_latency:.2f}s")
    print(f"FINAL FDE QUEST SCORE: {final_score} / 10,000")

if __name__ == "__main__":
    calculate_score()