# === FILE: myagents/maxmentor_agent.py ===
import os
import sys
import asyncio

# Add project root to sys.path for module imports (e.g., agents/)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel
from agents import function_tool

# === Load environment variables and disable tracing for local runs ===
load_dotenv()
set_tracing_disabled(True)

# === Load Gemini API key ===
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY is missing in .env")

# === Setup Gemini client ===
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# === Define model using Gemini ===
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# === Tool: Return trending AI tools ===
@function_tool
def fetch_ai_tools_news() -> str:
    """Fetch latest news about trending AI tools."""
    return "LangChain, OpenAI Agents SDK, and Claude 3.5 are trending tools this week."

# === Tool: Analyze trends in AI learning ===
@function_tool
def analyze_trends_in_learning(news: str = "") -> str:
    """Analyze what's currently trending in AI learning space."""
    return f"Based on tools like {news}, prompt engineering and agent-based development are hot topics."

# === Tool: Suggest learning paths ===
@function_tool
def suggest_learning_paths(analysis: str = "") -> str:
    """Suggest learning paths based on trend analysis."""
    return f"""
📘 **Learning Path Recommendation**

1. Learn Prompt Engineering basics  
2. Explore LangChain tutorials  
3. Build mini-projects using OpenAI Agents SDK  
4. Follow guides on Claude 3.5  
5. Stay updated via newsletters like Latent Space or TLDR.ai
"""

# === Define the MaxMentor Agent ===
maxmentor = Agent(
    name="MaxMentor",
    instructions="""
You are MaxMentor, an AI learning mentor.
1. Use `fetch_ai_tools_news` to get trending tools.
2. Use `analyze_trends_in_learning` to understand demand.
3. Use `suggest_learning_paths` to give practical steps.
Present it in Markdown for learners.
""",
    tools=[fetch_ai_tools_news, analyze_trends_in_learning, suggest_learning_paths],
    model=model
)

# === Manual run block ===
if __name__ == "__main__":
    async def main():
        print("📚 MaxMentor Agent Running...")
        result = await Runner.run(maxmentor, [{"role": "user", "content": "What's the best way to start learning AI today?"}])
        print("\n📢 Output:\n")
        print(result.final_output)

    asyncio.run(main())

# === Exported for main.py usage ===
# === Exported for main.py usage ===
# === Exported for main.py usage ===
async def run_agent(user_message: str = "What's the best way to start learning AI today?") -> str:
    result = await Runner.run(maxmentor, user_message)
    return result.final_output