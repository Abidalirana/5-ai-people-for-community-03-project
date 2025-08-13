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

# === Run all agents ===
async def run_all_agents():
    logging.info("🚀 Running all agents...")
    agents = [
        ("AtlasFX", run_atlasfx),
        ("CryptoNova", run_cryptonova),
        ("JaneMacro", run_janemacro),
        ("MaxMentor", run_maxmentor),
        ("QuantEdge", run_quantedge)
    ]

    for name, func in agents:
        try:
            logging.info(f"🔁 Running agent: {name}")
            output = await func()
            logging.info(f"✅ {name} Output:\n{output}\n")
        except Exception as e:
            logging.error(f"❌ Error in {name}: {e}")

# === Main Runner ===
async def main():
    scheduler = AsyncIOScheduler()

    # Run immediately
    scheduler.add_job(run_all_agents, trigger='date', run_date=datetime.now())

    # Then repeat every 6 hours
    scheduler.add_job(run_all_agents, trigger='interval', hours=6, next_run_time=datetime.now())

    scheduler.start()
    logging.info("🗓 Scheduler started. Runs all agents every 6 hours, first run immediately.")

    try:
        while True:
            await asyncio.sleep(3600)  # keep alive
    except (KeyboardInterrupt, SystemExit):
        logging.info("🛑 Scheduler stopped.")

if __name__ == "__main__":
    asyncio.run(main())
