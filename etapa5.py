"""Etapa 5: convolución entre señales aperiódicas intercambiando los roles."""
import numpy as np
from Señales import aperiodicas, t_h, dt
from etapa3 import energy, mean_power, lti_errors, slug
from pathlib import Path
import matplotlib.pyplot as plt
import csv

PAIRS = (
    ("Exp. decreciente", "Exp. creciente"),
    ("Exp. decreciente", "Escalón"),
    ("Exp. creciente", "Sinc"),
    ("Impulso", "Sinc"),
    ("Escalón", "Sinc"),
)

ROOT = Path(__file__).resolve().parent
FIG_DIR = ROOT / "resultados" / "etapa5" / "figuras"
CSV_PATH = ROOT / "resultados" / "etapa5" / "resultados_etapa5.csv"
FIRST_FIGURE = 48      # la etapa 4 termina en la Figura 47

def convolve(x, h):
    y = np.convolve(x, h) * dt
    t_y = 2 * t_h[0] + np.arange(y.size) * dt
    return t_y, y

def valid_range(x, h):
    """Rango [start, stop) de muestras de la salida que no dependen de tramos truncados."""
    start, stop = 0, x.size + h.size - 1
    x_first, x_last = np.flatnonzero(x)[[0, -1]]
    h_first, h_last = np.flatnonzero(h)[[0, -1]]
    x_left, x_right = x[0] != 0, x[-1] != 0
    h_left, h_right = h[0] != 0, h[-1] != 0
    if (x_right and h_left) or (x_left and h_right):
        return 0, 0
    if h_left:
        start = max(start, x_last)
    if x_left:
        start = max(start, h_last)
    if h_right:
        stop = min(stop, h.size + x_first)
    if x_right:
        stop = min(stop, x.size + h_first)
    return int(start), int(stop)

def plot_pair(number, a_name, a, b_name, b, t_y, y_ab, y_ba, start, stop):
    fig, axes = plt.subplots(3, 1, figsize=(8.2, 9.2))
    axes[0].plot(t_h, a, color="tab:blue")
    axes[0].set_title(f"Señal A: {a_name}")
    axes[0].set_ylabel("A(t) [u.a.]")
    axes[1].plot(t_h, b, color="tab:orange")
    axes[1].set_title(f"Señal B: {b_name}")
    axes[1].set_ylabel("B(t) [u.a.]")
    axes[2].plot(t_y, y_ab, color="tab:green", label="A * B (entrada A, sistema B)")
    axes[2].plot(t_y, y_ba, color="tab:purple", linestyle="--", label="B * A (entrada B, sistema A)")
    axes[2].set_title("Salidas")
    axes[2].set_ylabel("y(t) [u.a.]")
    label = "Afectado por el truncamiento"
    if start > 0:
        axes[2].axvspan(t_y[0], t_y[start], color="0.5", alpha=0.25, label=label)
        label = None
    if stop < y_ab.size:
        axes[2].axvspan(t_y[stop], t_y[-1], color="0.5", alpha=0.25, label=label)
    axes[2].legend(loc="upper right", fontsize=8)
    for axis in axes:
        axis.set_xlim(t_y[0], t_y[-1])
        axis.set_xlabel("Tiempo [s]")
        axis.grid(True, alpha=0.3)
    fig.suptitle(f"Figura {number}: {a_name} * {b_name}")
    fig.tight_layout()
    fig.savefig(FIG_DIR / f"fig{number:02d}_{slug(a_name)}_{slug(b_name)}.pdf", bbox_inches="tight")
    plt.close(fig)

def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    print("Conmutatividad: A*B contra B*A")
    rows = []
    for number, (a_name, b_name) in enumerate(PAIRS, start=FIRST_FIGURE):
        a = aperiodicas[a_name]
        b = aperiodicas[b_name]
        t_y, y_ab = convolve(a, b)
        _, y_ba = convolve(b, a)
        error = np.max(np.abs(y_ab - y_ba))
        lti_b = lti_errors(a, b)   # sistema B con entrada A
        lti_a = lti_errors(b, a)   # sistema A con entrada B
        start, stop = valid_range(a, b)
        print(f"{a_name} * {b_name}")
        print(f"  error de conmutatividad = {error:.1e}")
        print(f"  A: E = {energy(a):.5f}   P = {mean_power(a):.5f}")
        print(f"  B: E = {energy(b):.5f}   P = {mean_power(b):.5f}")
        print(f"  y: E = {energy(y_ab):.5f}   P = {mean_power(y_ab):.5f}")
        print(f"  LTI sistema B (aditividad, homogeneidad, invariancia): {max(lti_b):.1e}")
        print(f"  LTI sistema A (aditividad, homogeneidad, invariancia): {max(lti_a):.1e}")
        if stop > start:
            print(f"  zona válida: de {t_y[start]:.3f} a {t_y[stop - 1] + dt:.3f} s"
                  f"   E válida = {energy(y_ab[start:stop]):.5f}")
        else:
            print("  zona válida: no hay muestras válidas")
        plot_pair(number, a_name, a, b_name, b, t_y, y_ab, y_ba, start, stop)
        rows.append({
            "figura": number,
            "senal_a": a_name,
            "senal_b": b_name,
            "energia_a": energy(a),
            "potencia_a": mean_power(a),
            "energia_b": energy(b),
            "potencia_b": mean_power(b),
            "energia_salida": energy(y_ab),
            "potencia_salida": mean_power(y_ab),
            "energia_salida_valida": energy(y_ab[start:stop]) if stop > start else "",
            "error_conmutatividad": error,
            "error_lti_sistema_a": max(lti_a),
            "error_lti_sistema_b": max(lti_b),
        })
    with CSV_PATH.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Tabla guardada en {CSV_PATH}")
    print(f"Eje de salida: de {t_y[0]} a {t_y[-1]:.3f} s")


if __name__ == "__main__":
    main()