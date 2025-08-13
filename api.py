import json
import base64
import plotly.graph_objs as go
from fastapi import FastAPI
from pydantic import BaseModel

from myagents.atlasfx_agent import run_agent as run_atlasfx
from myagents.cryptonova_agent import run_agent as run_cryptonova
from myagents.janemacro_agent import run_agent as run_janemacro
from myagents.maxmentor_agent import run_agent as run_maxmentor
from myagents.quantedge_agent import run_agent as run_quantedge

from agents import Runner

app = FastAPI()

class UserQuery(BaseModel):
    message: str

async def run_agent_and_parse(agent_func, user_message: str):
    result = await Runner.run(agent_func, [{"role": "user", "content": user_message}])
    response_text = result.final_output

    summary = response_text
    img_b64 = None

    try:
        if "ChartData:" in response_text:
            summary_part, chart_json_part = response_text.split("ChartData:", 1)
            summary = summary_part.strip()

            chart_data = json.loads(chart_json_part.strip())

            if "chart_data" in chart_data:
                ohlc = chart_data["chart_data"]

                fig = go.Figure(data=[go.Candlestick(
                    x=[item["date"] for item in ohlc],
                    open=[item["open"] for item in ohlc],
                    high=[item["high"] for item in ohlc],
                    low=[item["low"] for item in ohlc],
                    close=[item["close"] for item in ohlc],
                )])

                img_bytes = fig.to_image(format="png")
                img_b64 = base64.b64encode(img_bytes).decode('utf-8')

    except Exception as e:
        print(f"⚠️ Warning: Failed to parse chart data or generate image: {e}")

    return {"summary": summary, "chart_image_base64": img_b64}

# Individual endpoints for each agent

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

# Combined endpoint to run all agents and return their results

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
