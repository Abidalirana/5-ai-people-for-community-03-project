# myagents/atlasfx_agent.py

import os
import sys
import asyncio

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

# === Simplified FX Tools ===

@function_tool
def fetch_fx_data(pair: str = "USD/JPY") -> str:
    """Fetch mock FX market data."""
    return f"{pair}: 150.50 | Vol: 2000 | 2025-07-31T12:00:00Z"

@function_tool
def analyze_fx_sentiment(price: float = 150.50) -> str:
    """Analyze sentiment based on FX price."""
    sentiment = "bullish" if price > 150 else "bearish"
    return f"Sentiment: {sentiment}, Confidence: 85%"

@function_tool
def generate_fx_summary(pair: str = "USD/JPY", sentiment: str = "bullish") -> str:
    """Generate Markdown FX summary based on sentiment."""
    price = 150.50
    return f"""
# {pair} 4H Setup - 2025-07-31
**Pattern**: Ascending Triangle  
**Entry**: {price}  
**Stop Loss**: {price - 0.5}  
**Take Profit**: {price + 1.5}  
**R:R**: 3:1  
**Logic**: {sentiment.capitalize()} outlook based on technicals.
""".strip()

# === Agent Setup ===
atlasfx = Agent(
    name="AtlasFX",
    instructions="""
You are a professional Forex market analyst.
1. Use `fetch_fx_data` to get latest FX stats.
2. Use `analyze_fx_sentiment` based on price.
3. Generate a summary with `generate_fx_summary`.
Always return an actionable trading insight.
""",
    tools=[fetch_fx_data, analyze_fx_sentiment, generate_fx_summary],
    model=model
)

# === Runner ===
if __name__ == "__main__":
    async def main():
        print("📈 AtlasFX Agent Running...")
        result = await Runner.run(atlasfx, [{"role": "user", "content": "What is the current USD/JPY sentiment?"}])
        print("\n📢 Output:\n")
        print(result.final_output)

    asyncio.run(main())
#=============================
#for testing in main.py
# Exported function for use in main.py
async def run_agent():
    result = await Runner.run(atlasfx, [{"role": "user", "content": "What is the current USD/JPY sentiment?"}])
    return result.final_output
