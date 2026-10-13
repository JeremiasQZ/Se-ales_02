"""Etapa 3: convolución de las señales periódicas con las cinco respuestas.

Genera figuras PDF vectoriales y una tabla CSV. Ejecutar desde la raíz del repo:
    python etapa3.py
"""
from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt
from Señales import periodicas, aperiodicas, t_x, t_h, dt, fs

ROOT = Path(__file__).resolve().parent
FIG_DIR = ROOT / "figuras_etapa3"
FIG_DIR.mkdir(exist_ok=True)
CSV_PATH = ROOT / "resultados_etapa3.csv"


def energy(signal_values):
    return float(np.sum(np.abs(signal_values) ** 2) * dt)


def mean_power(signal_values, time_values):
    duration = (time_values[-1] - time_values[0]) + dt
    return energy(signal_values) / duration


def lti_errors(x, h):
    """Return relative superposition and time-shift errors for y=x*h."""
    rng = np.random.default_rng(2026)
    x2 = rng.normal(size=x.size)
    a, b = 1.7, -0.45
    lhs = np.convolve(a * x + b * x2, h) * dt
    rhs = a * np.convolve(x, h) * dt + b * np.convolve(x2, h) * dt
    linearity = np.linalg.norm(lhs - rhs) / max(np.linalg.norm(lhs), 1e-15)

    shift = 37
    x_shifted = np.r_[np.zeros(shift), x]
    y_shifted = np.convolve(x_shifted, h) * dt
    y = np.convolve(x, h) * dt
    expected = np.r_[np.zeros(shift), y]
    invariance = np.linalg.norm(y_shifted - expected) / max(np.linalg.norm(y_shifted), 1e-15)
    return linearity, invariance


rows = []
for x_name, x in periodicas.items():
    for h_name, h in aperiodicas.items():
        y = np.convolve(x, h) * dt
        t_y = t_x[0] + t_h[0] + np.arange(y.size) * dt
        linearity, invariance = lti_errors(x, h)
        rows.append({
            "entrada": x_name,
            "respuesta": h_name,
            "energia_entrada": energy(x),
            "potencia_entrada": mean_power(x, t_x),
            "energia_salida": energy(y),
            "potencia_salida": mean_power(y, t_y),
            "error_linealidad": linearity,
            "error_invariancia": invariance,
        })

        fig, axes = plt.subplots(3, 1, figsize=(8.2, 8.2), sharex=False)
        axes[0].plot(t_x, x, color="tab:blue")
        axes[0].set_title(f"Entrada: {x_name}")
        axes[0].set_ylabel("Amplitud")
        axes[1].plot(t_h, h, color="tab:orange")
        axes[1].set_title(f"Respuesta a impulso: {h_name}")
        axes[1].set_ylabel("Amplitud")
        axes[2].plot(t_y, y, color="tab:green")
        axes[2].set_title("Salida: $y(t)=x(t)*h(t)$")
        axes[2].set_xlabel("Tiempo [s]")
        axes[2].set_ylabel("Amplitud")
        for axis in axes:
            axis.grid(True, alpha=0.3)
        fig.suptitle(f"Etapa 3 — {x_name} * {h_name}")
        fig.tight_layout()
        filename = f"{x_name}_{h_name}".replace(" ", "_").replace(".", "")
        fig.savefig(FIG_DIR / f"{filename}.pdf", bbox_inches="tight")
        plt.close(fig)

with CSV_PATH.open("w", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Generadas {len(rows)} convoluciones en {FIG_DIR}")
print(f"Tabla guardada en {CSV_PATH}")
print(f"fs={fs} Hz, dt={dt} s, salida: len(x)+len(h)-1 muestras")
