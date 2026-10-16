"""Etapas 1 y 2: gráficos de las señales base del laboratorio.

Las señales se definen en Señales.py; este script solo las grafica:
  - Figura 1: las cuatro señales periódicas de entrada (etapa 1).
  - Figura 2: las cinco señales aperiódicas, que en las etapas siguientes se
    usan como respuestas a impulso h(t) (etapa 2).

Las figuras se guardan como PDF vectorial en resultados/etapa1_2/.
Ejecutar desde la raíz del repo:
    python etapa1_2.py
"""
from pathlib import Path
import matplotlib.pyplot as plt
from Señales import periodicas, aperiodicas, t_x, t_h

OUT_DIR = Path(__file__).resolve().parent / "resultados" / "etapa1_2"


def plot_signals(number, title, t, signals, ylabel, path):
    """One panel per signal, sharing the time axis."""
    fig, axs = plt.subplots(len(signals), 1, figsize=(8, 2 * len(signals)), sharex=True)
    for ax, (nombre, values) in zip(axs, signals.items()):
        ax.plot(t, values)
        ax.set_title(nombre)
        ax.set_ylabel(ylabel)
        ax.grid(True)
    axs[-1].set_xlabel("Tiempo [s]")
    fig.suptitle(f"Figura {number}: {title}")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # Etapa 1: entradas periódicas, 4 periodos de f0 = 2 Hz en t = [0, 2) s.
    plot_signals(1, "señales periódicas de entrada", t_x, periodicas,
                 "x(t) [u.a.]", OUT_DIR / "fig01_periodicas.pdf")
    # Etapa 2: señales aperiódicas en t = [-1, 3) s. Como respuestas a impulso
    # tienen unidades de 1/s; el impulso mide 1/dt = 1000 para que su área sea 1.
    plot_signals(2, "señales aperiódicas (respuestas a impulso)", t_h, aperiodicas,
                 "h(t) [1/s]", OUT_DIR / "fig02_aperiodicas.pdf")
    print(f"Figuras 1 y 2 guardadas en {OUT_DIR}")


if __name__ == "__main__":
    main()
