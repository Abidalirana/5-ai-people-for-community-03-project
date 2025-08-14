import os
import json
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from myagents.atlasfx_agent import run_agent as run_atlasfx
from myagents.cryptonova_agent import run_agent as run_cryptonova
from myagents.janemacro_agent import run_agent as run_janemacro
from myagents.maxmentor_agent import run_agent as run_maxmentor
from myagents.quantedge_agent import run_agent as run_quantedge
from myagents.fx_graphs import plot_fx_setup
 #####
# === FastAPI app ===
app = FastAPI()

# === Expose charts folder as static files ===
CHARTS_DIR = os.path.join(os.path.dirname(__file__), "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)
app.mount("/charts", StaticFiles(directory=CHARTS_DIR), name="charts")

# === User query schema ===
class UserQuery(BaseModel):
    message: str

# === Run agent and return summary + chart URLs ===
async def run_agent_and_parse(agent_func, user_message: str):
    # Call agent function directly
    response_text = await agent_func(user_message)

    summary = response_text
    chart_urls = []

    try:
        if "ChartData:" in response_text:
            summary_part, chart_json_part = response_text.split("ChartData:", 1)
            summary = summary_part.strip()
            chart_data = json.loads(chart_json_part.strip())

            if "chart_data" in chart_data:
                for entry in chart_data["chart_data"]:
                    filename = f"{entry['pair'].replace('/', '')}_{entry['source']}.png"
                    file_path = os.path.join(CHARTS_DIR, filename)

                    # Save matplotlib chart (replace with your plotting function)
                    entry["save_path"] = file_path
                    plot_fx_setup(entry['pair'], entry['price'], save_path=file_path)    ###

                    chart_urls.append(f"/charts/{filename}")

    except Exception as e:
        print(f"⚠️ Warning: Failed to generate chart URLs: {e}")

    return {"summary": summary, "chart_urls": chart_urls}

# === Individual endpoints ===
@app.post("/run-atlasfx")
async def run_atlasfx_agent(query: UserQuery):
    return await run_agent_and_parse(run_atlasfx, query.message)

@app.post("/run-cryptonova")
async def run_cryptonova_agent(query: UserQuery):
    return await run_agent_and_parse(run_cryptonova, query.message)

@app.post("/run-janemacro")
async def run_janemacro_agent(query: UserQuery):
    return await run_agent_and_parse(run_janemacro, query.message)

@app.post("/run-maxmentor")
async def run_maxmentor_agent(query: UserQuery):
    return await run_agent_and_parse(run_maxmentor, query.message)

@app.post("/run-quantedge")
async def run_quantedge_agent(query: UserQuery):
    return await run_agent_and_parse(run_quantedge, query.message)

# === Combined endpoint ===
@app.post("/run-all-agents")
async def run_all_agents(query: UserQuery):
    agents = [
        ("AtlasFX", run_atlasfx),
        ("CryptoNova", run_cryptonova),
        ("JaneMacro", run_janemacro),
        ("MaxMentor", run_maxmentor),
        ("QuantEdge", run_quantedge),
    ]

    results = {}
    for name, agent_func in agents:
        results[name] = await run_agent_and_parse(agent_func, query.message)
    return results
