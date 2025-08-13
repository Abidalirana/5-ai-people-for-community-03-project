# myagents/cryptonova_agent.py

import os
import sys
import asyncio
import random

# Ensure parent directory is in sys.path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel
from agents import function_tool

# === Load environment variables and disable tracing for cleaner logs ===
load_dotenv()
set_tracing_disabled(True)

# === Read Gemini API key from environment ===
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY is missing in .env")

# === Setup Gemini-compatible OpenAI client ===
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# === Model configuration ===
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# === Tool: Fetch simulated cryptocurrency prices ===
@function_tool
def fetch_crypto_data() -> str:
    """Fetch simulated crypto prices for multiple symbols."""
    symbols = ["BTC", "ETH", "SOL", "ADA", "XRP"]
    prices = {sym: round(random.uniform(100, 3000), 2) for sym in symbols}
    return "📊 Prices: " + ", ".join([f"{s}: ${p}" for s, p in prices.items()])

# === Tool: Analyze trends based on fetched data ===
@function_tool
def analyze_crypto_trends(data: str = "") -> str:
    """Analyze crypto market trends based on price data."""
    if "BTC" in data and "ETH" in data:
        return "📈 BTC and ETH showing bullish momentum due to volume surge."
    return "📉 Market trend is currently neutral or mixed."

# === Tool: Summarize trending crypto news ===
@function_tool
def summarize_crypto_news() -> str:
    """Summarize key crypto news headlines."""
    headlines = [
        "Bitcoin ETF gains traction in global markets",
        "Ethereum 2.0 staking hits record high",
        "Solana partners with Visa for payments",
        "Regulatory pressure increases on altcoins"
    ]
    return "📰 Top Crypto News:\n" + "\n".join(f"- {h}" for h in headlines)

# === NEW TOOL: Generate sample crypto price data for charts ===
@function_tool
def generate_crypto_chart_data() -> dict:
    """
    Generate sample OHLC price data for BTC and ETH to be used in charts.
    This data will be returned as JSON-like dict for frontend plotting.
    """
    return {
        "BTC": {
            "dates": ["2025-08-08", "2025-08-09", "2025-08-10"],
            "open": [29000, 29100, 29250],
            "high": [29500, 29200, 29300],
            "low": [28800, 28900, 29000],
            "close": [29400, 29150, 29200]
        },
        "ETH": {
            "dates": ["2025-08-08", "2025-08-09", "2025-08-10"],
            "open": [1800, 1820, 1810],
            "high": [1850, 1830, 1825],
            "low": [1780, 1795, 1800],
            "close": [1840, 1815, 1810]
        }
    }

# === Define CryptoNova agent with all tools including chart data generator ===
cryptonova = Agent(
    name="CryptoNova",
    instructions="""
You are CryptoNova, a confident crypto analyst and educator.
1. Use `fetch_crypto_data` to get live prices.
2. Analyze trends with `analyze_crypto_trends`.
3. Summarize news with `summarize_crypto_news`.
4. Generate price chart data with `generate_crypto_chart_data`.
Return your output as a JSON object with keys:
- "summary": your tweet thread text
- "chart_data": the price data for BTC and ETH
Format your final response accordingly for easy parsing.
""",
    tools=[fetch_crypto_data, analyze_crypto_trends, summarize_crypto_news, generate_crypto_chart_data],
    model=model
)

# === Runner function to call from main.py or API ===
async def run_agent(user_message: str = "What’s the latest crypto update?") -> str:
    """Run the CryptoNova agent with a user message."""
    result = await Runner.run(cryptonova, user_message)
    return result.final_output

# === Local test runner (for development only) ===
if __name__ == "__main__":
    async def main():
        print("🚀 CryptoNova Agent Running...")
        result = await Runner.run(cryptonova, [{"role": "user", "content": "What’s the latest crypto update?"}])
        print("\n📢 Output:\n")
        print(result)

    asyncio.run(main())
