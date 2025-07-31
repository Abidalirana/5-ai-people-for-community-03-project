# === FILE: myagents/cryptonova_agent.py ===
import os
import sys
import asyncio
import random

# Ensure parent dir is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel
from agents import function_tool

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
def fetch_crypto_data() -> str:
    """Fetch simulated cryptocurrency market data."""
    symbols = ["BTC", "ETH", "SOL", "ADA", "XRP"]
    prices = {sym: round(random.uniform(100, 3000), 2) for sym in symbols}
    return "📊 Prices: " + ", ".join([f"{s}: ${p}" for s, p in prices.items()])

@function_tool
def analyze_crypto_trends(data: str = "") -> str:
    """Analyze trends based on market data."""
    if "BTC" in data and "ETH" in data:
        return "📈 BTC and ETH showing bullish momentum due to volume surge."
    return "📉 Market trend is currently neutral or mixed."

@function_tool
def summarize_crypto_news() -> str:
    """Summarize trending crypto news."""
    headlines = [
        "Bitcoin ETF gains traction in global markets",
        "Ethereum 2.0 staking hits record high",
        "Solana partners with Visa for payments",
        "Regulatory pressure increases on altcoins"
    ]
    return "📰 Top Crypto News:\n" + "\n".join(f"- {h}" for h in headlines)

# === Agent Setup ===
cryptonova = Agent(
    name="CryptoNova",
    instructions="""
You are CryptoNova, a confident crypto analyst and educator.
1. Use `fetch_crypto_data` to get live prices.
2. Analyze trends with `analyze_crypto_trends`.
3. Summarize news with `summarize_crypto_news`.
Format everything like a tweet thread for a crypto-savvy audience.
""",
    tools=[fetch_crypto_data, analyze_crypto_trends, summarize_crypto_news],
    model=model
)

# === Runner ===
if __name__ == "__main__":
    async def main():
        print("🚀 CryptoNova Agent Running...")
        result = await Runner.run(cryptonova, [{"role": "user", "content": "What’s the latest crypto update?"}])
        print("\n📢 Output:\n")
        print(result.final_output)

    asyncio.run(main())
#=======================
# Exported function for use in main.py
async def run_agent():
    result = await Runner.run(
        cryptonova,
        [{"role": "user", "content": "What’s the latest crypto update?"}]
    )
    return result.final_output
