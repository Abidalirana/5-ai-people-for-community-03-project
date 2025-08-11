import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import logging

# === Import agent run functions ===
from myagents.atlasfx_agent import run_agent as run_atlasfx
from myagents.cryptonova_agent import run_agent as run_cryptonova
from myagents.janemacro_agent import run_agent as run_janemacro
from myagents.maxmentor_agent import run_agent as run_maxmentor
from myagents.quantedge_agent import run_agent as run_quantedge

# === Setup Logging ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# === Async Job Wrapper ===
async def run_and_log(agent_name, run_func):
    logging.info(f"🔁 Running agent: {agent_name}")
    try:
        output = await run_func()
        logging.info(f"✅ {agent_name} Output:\n{output}\n")
    except Exception as e:
        logging.error(f"❌ Error in {agent_name}: {e}")

# === Job Scheduler Helper ===
def schedule_agent(scheduler, agent_name, run_func, interval_seconds=60):
    async def job():
        await run_and_log(agent_name, run_func)

    scheduler.add_job(
        job,
        trigger='interval',
        seconds=interval_seconds,
        next_run_time=datetime.now()
    )

# === Main Runner ===
async def main():
    scheduler = AsyncIOScheduler()

    schedule_agent(scheduler, "AtlasFX", run_atlasfx, interval_seconds=120)
    schedule_agent(scheduler, "CryptoNova", run_cryptonova, interval_seconds=180)
    schedule_agent(scheduler, "JaneMacro", run_janemacro, interval_seconds=300)
    schedule_agent(scheduler, "MaxMentor", run_maxmentor, interval_seconds=240)
    schedule_agent(scheduler, "QuantEdge", run_quantedge, interval_seconds=150)

    scheduler.start()
    logging.info("🚀 Scheduler started.")

    try:
        while True:
            await asyncio.sleep(3600)  # keep loop alive
    except (KeyboardInterrupt, SystemExit):
        logging.info("🛑 Scheduler stopped.")

# === Entry Point ===
if __name__ == "__main__":
    asyncio.run(main())
