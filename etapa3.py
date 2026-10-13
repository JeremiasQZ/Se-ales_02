"""Etapa 3: convolución de las señales periódicas con las cinco respuestas.

Genera figuras PDF vectoriales y una tabla CSV en resultados/etapa3/.
Ejecutar desde la raíz del repo:
    python etapa3.py

Las funciones se pueden importar desde otras etapas sin ejecutar el script:
    from etapa3 import energy, convolve, power_window, valid_range, lti_errors
"""
from pathlib import Path
import csv
import unicodedata
import numpy as np
import matplotlib.pyplot as plt
from Señales import periodicas, aperiodicas, t_x, t_h, dt, fs, T0

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "resultados" / "etapa3"
FIG_DIR = OUT_DIR / "figuras"
CSV_PATH = OUT_DIR / "resultados_etapa3.csv"
FIRST_FIGURE = 3                      # las figuras 1 y 2 son las de etapa1_2.py
N_PERIOD = int(round(T0 / dt))        # muestras por periodo de la entrada


def energy(signal_values):
    return float(np.sum(np.abs(signal_values) ** 2) * dt)


def mean_power(signal_values):
    """Mean power over the whole vector: energy divided by its duration."""
    return energy(signal_values) / (np.size(signal_values) * dt)


def convolve(x, h):
    """Return (t_y, y) with y = x*h approximating the continuous convolution."""
    y = np.convolve(x, h) * dt
    t_y = t_x[0] + t_h[0] + np.arange(y.size) * dt
    return t_y, y


def valid_range(h):
    """Return the output sample range [start, stop) not affected by truncating h.

    If h is still nonzero at an edge of its window, the ideal h continues beyond
    it and the output samples that would need that missing part are artifacts.
    """
    start, stop = 0, t_x.size + h.size - 1
    if h[0] != 0:                     # truncada por la izquierda (sinc)
        start = t_x.size - 1
    if h[-1] != 0:                    # truncada por la derecha (escalón, sinc)
        stop = h.size
    return start, stop


def power_window(h):
    """Return (start, stop, kind): output sample range used for the mean power.

    Steady state exists where every nonzero sample of h overlaps the input. If h
    lasts longer than the input there is none, and the window is the interval
    where the input is present, restricted to valid_range. In both cases the
    window is trimmed to a whole number of periods.
    """
    support = np.flatnonzero(h)
    start, stop = support[-1], support[0] + t_x.size
    kind = "régimen permanente"
    if stop - start < N_PERIOD:
        input_start = int(round(-t_h[0] / dt))
        valid_start, valid_stop = valid_range(h)
        start = max(input_start, valid_start)
        stop = min(input_start + t_x.size, valid_stop)
        kind = "transitoria"
    periods = (stop - start) // N_PERIOD
    return start, start + periods * N_PERIOD, kind


def lti_errors(x, h):
    """Return max abs errors of additivity, homogeneity and time invariance."""
    rng = np.random.default_rng(2026)
    x2 = rng.normal(size=x.size)
    a = 1.7
    y = np.convolve(x, h) * dt
    y2 = np.convolve(x2, h) * dt
    additivity = np.max(np.abs(np.convolve(x + x2, h) * dt - (y + y2)))
    homogeneity = np.max(np.abs(np.convolve(a * x, h) * dt - a * y))

    shift = 37
    y_shifted = np.convolve(np.r_[np.zeros(shift), x], h) * dt
    invariance = np.max(np.abs(y_shifted - np.r_[np.zeros(shift), y]))
    return float(additivity), float(homogeneity), float(invariance)


def slug(text):
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return ascii_text.lower().replace(".", "").replace(" ", "_")


def plot_case(number, x_name, x, h_name, h, t_y, y):
    start, stop, kind = power_window(h)
    valid_start, valid_stop = valid_range(h)

    fig, axes = plt.subplots(3, 1, figsize=(8.2, 9.2))
    axes[0].plot(t_x, x, color="tab:blue")
    axes[0].set_title(f"Entrada: {x_name}")
    axes[0].set_ylabel("x(t) [u.a.]")
    axes[1].plot(t_h, h, color="tab:orange")
    axes[1].set_title(f"Respuesta a impulso: {h_name}")
    axes[1].set_ylabel("h(t) [1/s]")
    axes[2].plot(t_y, y, color="tab:green")
    axes[2].set_title("Salida: $y(t)=x(t)*h(t)$")
    axes[2].set_ylabel("y(t) [u.a.]")
    axes[2].axvspan(t_y[start], t_y[stop - 1] + dt, color="tab:green", alpha=0.15,
                    label=f"Ventana de potencia ({kind})")
    label = "Afectado por el truncamiento de h(t)"
    if valid_start > 0:
        axes[2].axvspan(t_y[0], t_y[valid_start], color="0.5", alpha=0.25, label=label)
        label = None
    if valid_stop < y.size:
        axes[2].axvspan(t_y[valid_stop], t_y[-1], color="0.5", alpha=0.25, label=label)
    axes[2].legend(loc="upper right", fontsize=8)
    for axis in axes:
        axis.set_xlim(t_y[0], t_y[-1])
        axis.set_xlabel("Tiempo [s]")
        axis.grid(True, alpha=0.3)
    fig.suptitle(f"Figura {number}: {x_name} * {h_name}")
    fig.tight_layout()
    path = FIG_DIR / f"fig{number:02d}_{slug(x_name)}_{slug(h_name)}.pdf"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    number = FIRST_FIGURE
    for x_name, x in periodicas.items():
        for h_name, h in aperiodicas.items():
            t_y, y = convolve(x, h)
            start, stop, kind = power_window(h)
            valid_start, valid_stop = valid_range(h)
            additivity, homogeneity, invariance = lti_errors(x, h)
            rows.append({
                "figura": number,
                "entrada": x_name,
                "respuesta": h_name,
                "energia_entrada": energy(x),
                "potencia_entrada": mean_power(x),
                "energia_salida": energy(y),
                "energia_salida_valida": energy(y[valid_start:valid_stop]),
                "potencia_salida": mean_power(y[start:stop]),
                "ventana_inicio_s": round(float(t_y[start]), 6),
                "ventana_fin_s": round(float(t_y[stop - 1] + dt), 6),
                "tipo_ventana": kind,
                "error_aditividad": additivity,
                "error_homogeneidad": homogeneity,
                "error_invariancia": invariance,
            })
            plot_case(number, x_name, x, h_name, h, t_y, y)
            number += 1

    with CSV_PATH.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"{'Fig':>3} {'Entrada':17s}{'Respuesta':17s}{'E_ent':>8}{'P_ent':>8}"
          f"{'E_sal':>10}{'E_sal_val':>10}{'P_sal':>10}  Ventana [s]")
    for row in rows:
        print(f"{row['figura']:>3} {row['entrada']:17s}{row['respuesta']:17s}"
              f"{row['energia_entrada']:8.4f}{row['potencia_entrada']:8.4f}"
              f"{row['energia_salida']:10.5f}{row['energia_salida_valida']:10.5f}"
              f"{row['potencia_salida']:10.6f}  "
              f"[{row['ventana_inicio_s']:.3f}, {row['ventana_fin_s']:.3f}) {row['tipo_ventana']}")
    for key in ("error_aditividad", "error_homogeneidad", "error_invariancia"):
        print(f"Máximo {key}: {max(row[key] for row in rows):.2e}")
    print(f"Generadas {len(rows)} convoluciones en {FIG_DIR}")
    print(f"Tabla guardada en {CSV_PATH}")
    print(f"fs={fs} Hz, dt={dt} s, salida: len(x)+len(h)-1 muestras")


if __name__ == "__main__":
    main()
