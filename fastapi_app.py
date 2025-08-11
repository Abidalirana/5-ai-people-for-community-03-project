#fastapi_app.py
from fastapi import FastAPI
from pydantic import BaseModel
from myagents.atlasfx_agent import atlasfx
from agents import Runner

app = FastAPI()

class UserQuery(BaseModel):
    message: str

@app.post("/run-agent")
async def run_agent(query: UserQuery):
    result = await Runner.run(atlasfx, [{"role": "user", "content": query.message}])
    return {"response": result.final_output}





