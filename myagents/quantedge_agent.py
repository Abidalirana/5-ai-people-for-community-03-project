# === FILE: myagents/quantedge_agent.py ===
import os
import sys
import asyncio

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

# === Tools ===

@function_tool
def fetch_quantsignal_data() -> str:
    """Fetch recent quant signal data including indicators, volatility, and asset targets."""
    return (
        "📊 Quant Signals:\n"
        "- MACD bullish crossover on SPY\n"
        "- High volatility alert on TSLA\n"
        "- RSI oversold on AAPL"
    )

@function_tool
def analyze_quant_models(data: str = "") -> str:
    """Analyze quant models and return metrics like Sharpe ratio, drawdown, and alpha."""
    return (
        "📈 Quant Model Analysis:\n"
        "- Sharpe Ratio: 1.42\n"
        "- Max Drawdown: 7.5%\n"
        "- Annualized Alpha: 3.1%"
    )

@function_tool
def summarize_edge_cases() -> str:
    """Summarize special edge cases or anomalies detected in quant data."""
    return (
        "⚠️ Edge Case Summary:\n"
        "- Anomaly in BTC volatility spike (20% in 1 day)\n"
        "- Unexpected drawdown in momentum strategy"
    )

# === Agent Setup ===
quantedge = Agent(
    name="QuantEdge",
    instructions="""
You are QuantEdge, a precise quant researcher:
1. Use `fetch_quantsignal_data` for market signals.
2. Use `analyze_quant_models` to assess strategies.
3. Use `summarize_edge_cases` for anomalies.
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
    result = await Runner.run(quantedge, user_message)
    return result.final_output