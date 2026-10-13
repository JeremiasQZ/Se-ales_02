from pathlib import Path
import matplotlib.pyplot as plt
from Señales import *
OUT_DIR = Path(__file__).resolve().parent / "resultados" / "etapa1_2"
OUT_DIR.mkdir(parents=True, exist_ok=True)
fig, axs = plt.subplots(4, 1, figsize=(8, 8), sharex=True)
for ax, (nombre, x) in zip(axs, periodicas.items()):
    ax.plot(t_x, x); ax.set_title(nombre); ax.set_ylabel("Amplitud"); ax.grid(True)
axs[-1].set_xlabel("Tiempo [s]")
fig.tight_layout(); fig.savefig(OUT_DIR / "fig01_periodicas.pdf")
fig, axs = plt.subplots(5, 1, figsize=(8, 10), sharex=True)
for ax, (nombre, h) in zip(axs, aperiodicas.items()):
    ax.plot(t_h, h); ax.set_title(nombre); ax.set_ylabel("Amplitud"); ax.grid(True)
axs[-1].set_xlabel("Tiempo [s]")
fig.tight_layout(); fig.savefig(OUT_DIR / "fig02_aperiodicas.pdf")
 