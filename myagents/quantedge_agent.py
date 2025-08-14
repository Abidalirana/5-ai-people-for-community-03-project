# === FILE: myagents/quantedge_agent.py ============================================
import os
import sys
import asyncio
import json

# Ensure parent dir is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, function_tool

# === ENV & Config ===
load_dotenv()
set_tracing_disabled(True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY is missing in .env")

# === External Gemini Client ===
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# === Tools ============================================================================

@function_tool
def fetch_quantsignal_data() -> str:
    """Fetch recent quant signal data including indicators, volatility, and asset targets."""
    # Return signals as text and structured JSON (string)
    signals_text = (
        "📊 Quant Signals:\n"
        "- MACD bullish crossover on SPY\n"
        "- High volatility alert on TSLA\n"
        "- RSI oversold on AAPL"
    )
    # Example structured data for visualization
    signals_data = {
        "dates": ["2025-08-08", "2025-08-09", "2025-08-10", "2025-08-11"],
        "SPY_MACD": [0.1, 0.3, 0.5, 0.7],  # Example MACD values (rising)
        "TSLA_Volatility": [1.2, 1.5, 3.8, 4.0],  # Volatility spikes
        "AAPL_RSI": [65, 55, 30, 25]  # RSI dropping indicating oversold
    }
    # Attach JSON string to signals text for agent reference or external use
    return signals_text + "\n\n" + json.dumps(signals_data)

@function_tool
def analyze_quant_models(data: str = "") -> str:
    """Analyze quant models and return metrics like Sharpe ratio, drawdown, and alpha."""
    # Metrics text
    metrics_text = (
        "📈 Quant Model Analysis:\n"
        "- Sharpe Ratio: 1.42\n"
        "- Max Drawdown: 7.5%\n"
        "- Annualized Alpha: 3.1%"
    )
    # Structured metrics data (for charts like bar chart)
    metrics_data = {
        "Sharpe_Ratio": 1.42,
        "Max_Drawdown": 7.5,
        "Annualized_Alpha": 3.1
    }
    return metrics_text + "\n\n" + json.dumps(metrics_data)

@function_tool
def summarize_edge_cases() -> str:
    """Summarize special edge cases or anomalies detected in quant data."""
    # Summary text
    summary_text = (
        "⚠️ Edge Case Summary:\n"
        "- Anomaly in BTC volatility spike (20% in 1 day)\n"
        "- Unexpected drawdown in momentum strategy"
    )
    # Example markers for anomalies on chart (timestamps and description)
    anomalies = [
        {"date": "2025-08-09", "description": "BTC volatility spike 20%"},
        {"date": "2025-08-10", "description": "Momentum strategy drawdown"}
    ]
    return summary_text + "\n\n" + json.dumps(anomalies)

# === Agent Setup ===
quantedge = Agent(
    name="QuantEdge",
    instructions="""
You are QuantEdge, a precise quant researcher:
1. Use `fetch_quantsignal_data` for market signals (return both text + JSON data).
2. Use `analyze_quant_models` to assess strategies (return text + JSON).
3. Use `summarize_edge_cases` for anomalies (text + JSON).
Output should resemble a quant research digest with clear metrics.
""",
    tools=[fetch_quantsignal_data, analyze_quant_models, summarize_edge_cases],
    model=model
)

# === Runner (local test) ===
if __name__ == "__main__":
    async def main():
        print("📊 QuantEdge Agent Running...")
        result = await Runner.run(
            quantedge,
            "What's today’s quant signal summary?"
        )
        print("\n📢 Output:\n")
        print(result.final_output)

    asyncio.run(main())

# === Exported function for main.py ===
async def run_agent(user_message: str = "Give me today's market update") -> str:
    """
    Run the QuantEdge agent and return the final output,
    which includes text and embedded JSON strings for visualization.
    """
    result = await Runner.run(quantedge, user_message)
    return result.final_output
