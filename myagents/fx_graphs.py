import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Ensure WEB_CHARTS_DIR exists (should match the one in atlasfx_agent.py)
WEB_CHARTS_DIR = os.path.join(os.path.dirname(__file__), "charts")
os.makedirs(WEB_CHARTS_DIR, exist_ok=True)

def plot_fx_setup(pair: str, price: float, source: str = "Simulated", save_path: str = None) -> str:
    """
    Generate a simple FX 4H setup chart and return file path.
    Each chart filename is unique using source name and timestamp.
    If save_path is provided, save the chart there.
    """
    entry = price
    sl = entry - 0.5
    tp = entry + 1.5

    plt.figure(figsize=(6, 3.5))
    xs = ["T-1", "T", "T+1"]
    ys = [entry - 1, entry, entry + 1]
    plt.plot(xs, ys, marker="o", label=pair)

    for lvl, col, lbl in [(entry, "blue", "Entry"), (sl, "red", "SL"), (tp, "green", "TP")]:
        plt.axhline(lvl, color=col, linestyle="--", label=f"{lbl} {lvl:.4f}")

    plt.title(f"{pair} – 4H Setup ({source})")
    plt.legend()

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    fname = f"{pair.replace('/', '')}_{source}_{timestamp}.png"

    # If save_path is provided, use it; else save to WEB_CHARTS_DIR
    if save_path is None:
        save_path = os.path.join(WEB_CHARTS_DIR, fname)
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    return save_path