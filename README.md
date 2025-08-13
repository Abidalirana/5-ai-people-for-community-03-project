ai05_peolpe_03project/
│
├── .env
├── .gitignore
├── .python-version
├── main.py
├── pyproject.toml
├── README.md
├── scheduler.py
├── uv.lock
│
├── myagents/
│   ├── __init__.py
│   ├── atlasfx_agent.py
│   ├── cryptonova_agent.py
│   ├── janemacro_agent.py
│   ├── maxmentor_agent.py
│   ├── quantedge_agent.py

==================================
=================================================================================

=============================================================================================================================
==============================================================================================================================
my-project reference here 

1--
# myagents/atlasfx_agent.py

import os
import sys
import asyncio

# === Add parent directory to path for module access ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel
from agents import function_tool

# === Load environment variables and disable tracing ===
load_dotenv()
set_tracing_disabled(True)

# === Read Gemini API key from environment ===
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY is missing in .env")

# === Setup external Gemini-compatible OpenAI client ===
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# === Define model configuration ===
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# === Tool: Fetch mock FX data ===
@function_tool
def fetch_fx_data(pair: str = "USD/JPY") -> str:
    """Fetch mock FX market data."""
    return f"{pair}: 150.50 | Vol: 2000 | 2025-07-31T12:00:00Z"

# === Tool: Analyze sentiment based on price ===
@function_tool
def analyze_fx_sentiment(price: float = 150.50) -> str:
    """Analyze sentiment based on FX price."""
    sentiment = "bullish" if price > 150 else "bearish"
    return f"Sentiment: {sentiment}, Confidence: 85%"

# === Tool: Generate FX summary in Markdown ===
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

# === NEW Tool: Generate structured data for chart visualization ===
@function_tool
def generate_fx_chart_data(pair: str = "USD/JPY", price: float = 150.5, sentiment: str = "bullish") -> dict:
    """
    Generate structured JSON data for creating charts in FastAPI frontend.
    This returns entry, stop loss, take profit levels, and other info for plotting.
    """
    return {
        "pair": pair,
        "pattern": "Ascending Triangle",
        "entry": price,
        "stop_loss": price - 0.5,
        "take_profit": price + 1.5,
        "risk_reward": "3:1",
        "sentiment": sentiment,
        "confidence": 85
    }

# === Define AtlasFX agent with tools and logic ===
atlasfx = Agent(
    name="AtlasFX",
    instructions="""
You are a professional Forex market analyst.
1. Use `fetch_fx_data` to get latest FX stats.
2. Use `analyze_fx_sentiment` based on price.
3. Use `generate_fx_summary` to create a Markdown summary.
4. Use `generate_fx_chart_data` to create structured JSON data for charting.
Return a JSON object with two keys:
- 'summary': markdown summary string
- 'chart_data': JSON object for visualization
""",
    tools=[fetch_fx_data, analyze_fx_sentiment, generate_fx_summary, generate_fx_chart_data],
    model=model
)

# === Exported function to run agent and parse output for FastAPI ===
async def run_agent(user_message: str = "What’s the FX summary for USD/JPY?") -> dict:
    """
    Runs AtlasFX agent with the user message.
    Expects the agent to return a JSON string with 'summary' and 'chart_data'.
    Returns parsed dictionary with keys 'summary' and 'chart_data'.
    """
    result = await Runner.run(atlasfx, user_message)

    import json
    # Parse the JSON output safely
    try:
        output = json.loads(result.final_output)
    except Exception as e:
        # If output is not JSON, fallback to plain text summary and empty chart data
        output = {
            "summary": result.final_output,
            "chart_data": {}
        }
    return output


# === Local test runner (only runs when executing this file directly) ===
if __name__ == "__main__":
    from agents import ConversationSession

    async def main():
        print("📈 AtlasFX Agent Running...")

        # Create a test session with sample query
        session = ConversationSession("AtlasFX", messages=["What’s the FX summary for USD/JPY?"])

        result = await Runner.run(atlasfx, session)
        print("\n📢 Raw Output:\n")
        print(result)

        # Try parsing JSON output
        import json
        try:
            output = json.loads(result.final_output)
            print("\n✅ Parsed Output:\n")
            print(output)
        except Exception as e:
            print("\n❌ Failed to parse JSON output:", e)

    asyncio.run(main())
=============================================================================================================================
==============================================================================================================================
===============================================================
===============================================================





=============================================================================================================================
==============================================================================================================================




=============================================================================================================================
==============================================================================================================================





=============================================================================================================================
==============================================================================================================================




=============================================================================================================================
==============================================================================================================================