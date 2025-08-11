import os
import sys
import asyncio

# === Ensure parent directory is in sys.path for relative imports ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel
from agents import function_tool

# === Load environment variables ===
load_dotenv()
set_tracing_disabled(True)

# === Get Gemini API key from environment ===
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY is missing in .env")

# === Setup Gemini client with AsyncOpenAI ===
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# === Define the model configuration ===
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# === Define tools (functions) that agent will use ===

@function_tool
def fetch_macro_data() -> str:
    """Fetch recent macroeconomic indicators."""
    return """
- 🇺🇸 US GDP: 2.4% growth in Q2 2025  
- 📈 Inflation: 3.1%  
- 👷‍♂️ Unemployment: 3.5%  
- 🇪🇺 ECB Rate: Held steady at 4.5%
""".strip()

@function_tool
def analyze_policy_trends() -> str:
    """Analyze global fiscal and monetary trends."""
    return """
- 🏦 Fed likely to hold rates through Q4  
- 🇯🇵 BOJ expected to exit negative rates in 2026  
- 🇨🇳 China ramps up infrastructure stimulus
""".strip()

@function_tool
def summarize_macro_news() -> str:
    """Summarize key macroeconomic developments."""
    return """
📰 Macro Update:
- US economic growth exceeds forecasts  
- ECB maintains dovish tone  
- China prepares additional stimulus  
- Fed stays cautious amid stable inflation
""".strip()

# === Define the JaneMacro agent with tools and instructions ===
janemacro = Agent(
    name="JaneMacro",
    instructions="""
You are JaneMacro, a macroeconomic strategist and policy analyst.

Your task:
1. Use `fetch_macro_data` to gather key economic stats.
2. Use `analyze_policy_trends` to interpret central bank/fiscal policy direction.
3. Use `summarize_macro_news` to package it all into a markdown-style macro brief.

Make it concise and actionable for global investors and macro followers.
""",
    tools=[fetch_macro_data, analyze_policy_trends, summarize_macro_news],
    model=model
)

# === Optional: Run directly for testing this agent file ===
if __name__ == "__main__":
    async def main():
        print("🌍 JaneMacro Agent Running...")
        result = await Runner.run(janemacro, [{"role": "user", "content": "Give me a macroeconomic update"}])
        print("\n📢 Output:\n")
        print(result.final_output)

    asyncio.run(main())

# === Exported function to be used in main.py ===
# === Exported function to be used in main.py ===
async def run_agent(user_message: str = "Give me a macroeconomic update") -> str:
    """
    Run the JaneMacro agent and return the final output.
    This will be called from main.py or any external script.
    """
    result = await Runner.run(janemacro, user_message)
    return result.final_output
