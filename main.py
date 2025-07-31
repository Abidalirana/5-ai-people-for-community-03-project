# main.py
import asyncio
from myagents.atlasfx_agent import run_agent as run_atlasfx
from myagents.cryptonova_agent import run_agent as run_cryptonova
from myagents.janemacro_agent import run_agent as run_janemacro
from myagents.maxmentor_agent import run_agent as run_maxmentor
from myagents.quantedge_agent import run_agent as run_quantedge

async def main():
    print("🟦 Running AtlasFX Agent...")
    atlas_result = await run_atlasfx()
    print("Result from AtlasFX:\n", atlas_result, "\n")

    print("🟨 Running CryptoNova Agent...")
    crypto_result = await run_cryptonova()
    print("Result from CryptoNova:\n", crypto_result, "\n")

    print("🟩 Running JaneMacro Agent...")
    jane_result = await run_janemacro()
    print("Result from JaneMacro:\n", jane_result, "\n")

    print("🟧 Running MaxMentor Agent...")
    mentor_result = await run_maxmentor()
    print("Result from MaxMentor:\n", mentor_result, "\n")

    print("🟥 Running QuantEdge Agent...")
    quant_result = await run_quantedge()
    print("Result from QuantEdge:\n", quant_result, "\n")

if __name__ == "__main__":
    asyncio.run(main())
