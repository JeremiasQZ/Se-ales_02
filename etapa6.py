"""Etapa 6: respuesta en frecuencia de los cinco sistemas, como apoyo al análisis.

Calcula H(jw) = sum h(t) e^{-jwt} dt a partir de las mismas h muestreadas de
Señales.py, y genera una figura y una tabla en resultados/etapa6/.
Ejecutar desde la raíz del repo:
    python etapa6.py
"""
from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt
from Señales import aperiodicas, t_h, dt, f0

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "resultados" / "etapa6"
FIG_PATH = OUT_DIR / "fig53_respuesta_en_frecuencia.pdf"
CSV_PATH = OUT_DIR / "respuesta_en_frecuencia.csv"
HARMONICS = (1, 2, 3, 5)      # armónicos de f0 que se tabulan


def frequency_response(h, f):
    """Return H(j2πf) for the sampled impulse response h on t_h."""
    f = np.atleast_1d(f)
    return np.sum(h * np.exp(-2j * np.pi * np.outer(f, t_h)), axis=1) * dt


def plot_responses():
    f = np.linspace(0, 10, 2001)
    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    for name, h in aperiodicas.items():
        ax.semilogy(f, np.maximum(np.abs(frequency_response(h, f)), 1e-4), label=name)
    for k in range(1, 6):
        ax.axvline(k * f0, color="0.6", linestyle=":", linewidth=1)
    ax.set_xlim(f[0], f[-1])
    ax.set_ylim(1e-4, 10)
    ax.set_xlabel("Frecuencia [Hz]")
    ax.set_ylabel("|H(f)| [adim.]")
    ax.set_title("Figura 53: magnitud de la respuesta en frecuencia de los cinco sistemas\n"
                 "(líneas punteadas: f0 = 2 Hz y sus armónicos)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG_PATH, bbox_inches="tight")
    plt.close(fig)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, h in aperiodicas.items():
        row = {"sistema": name, "ganancia_dc": float(frequency_response(h, 0)[0].real)}
        for k in HARMONICS:
            value = frequency_response(h, k * f0)[0]
            row[f"modulo_{k}f0"] = float(abs(value))
            row[f"fase_{k}f0_grados"] = float(np.degrees(np.angle(value))) if abs(value) > 1e-9 else ""
        rows.append(row)

    with CSV_PATH.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    plot_responses()

    print(f"{'Sistema':17s}{'DC':>8}" + "".join(f"{f'|H({k}f0)|':>11}{'fase':>9}" for k in HARMONICS))
    for row in rows:
        line = f"{row['sistema']:17s}{row['ganancia_dc']:8.4f}"
        for k in HARMONICS:
            phase = row[f"fase_{k}f0_grados"]
            line += f"{row[f'modulo_{k}f0']:11.5f}" + (f"{phase:8.2f}°" if phase != "" else f"{'-':>9}")
        print(line)
    print(f"Figura guardada en {FIG_PATH}")
    print(f"Tabla guardada en {CSV_PATH}")


if __name__ == "__main__":
    main()
