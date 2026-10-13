"""Etapa 4: factor de proporcionalidad y corrimiento temporal en h(t).

Genera figuras PDF vectoriales y tablas CSV en resultados/etapa4/.
Ejecutar desde la raíz del repo:
    python etapa4.py
"""
from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt
from Señales import (periodicas, aperiodicas, t_x, t_h, dt, T0,
                     exp_decreciente, exp_creciente, impulso, escalon, sinc)
from etapa3 import (energy, mean_power, convolve, power_window, valid_range,
                    slug, FIRST_FIGURE)

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "resultados" / "etapa4"
FIG_DIR = OUT_DIR / "figuras"
CSV_SCALING = OUT_DIR / "resultados_etapa4_escalamiento.csv"
CSV_SHIFTING = OUT_DIR / "resultados_etapa4_corrimiento.csv"
CSV_SUMMARY = OUT_DIR / "resumen_etapa4.csv"
FIRST_FIGURE_4 = FIRST_FIGURE + len(periodicas) * len(aperiodicas)   # sigue a la etapa 3
FIGURE_INPUTS = ("Senoidal",)   # entradas que se grafican; la tabla usa las cuatro

A_VALUES = (2, 0.5, -1)      # factores de proporcionalidad; -1 invierte el signo
T0_VALUES = (0.1, 0.25)      # corrimientos [s]; 0.25 s = T0/2

# Las mismas respuestas de Señales.py, pero como funciones de t, para poder
# evaluarlas en (t - t0). El orden y los nombres coinciden con `aperiodicas`.
RESPUESTAS = {
    "Exp. decreciente": exp_decreciente,
    "Exp. creciente": exp_creciente,
    "Impulso": impulso,
    "Escalón": escalon,
    "Sinc": sinc,
}


def modified_h(h_name, a=1.0, t0=0.0):
    """Return a*h(t - t0) sampled on t_h."""
    return a * RESPUESTAS[h_name](t_h - t0)


def output_metrics(x, h):
    """Return (t_y, y, total energy, valid energy, window power) for y = x*h."""
    t_y, y = convolve(x, h)
    start, stop, _ = power_window(h)
    valid_start, valid_stop = valid_range(h)
    return (t_y, y, energy(y), energy(y[valid_start:valid_stop]),
            mean_power(y[start:stop]))


def check_base():
    """Paso 1: con a=1 y t0=0 se deben recuperar las h y salidas de la etapa 3."""
    print("Paso 1: caso base (a=1, t0=0) contra la etapa 3")
    for h_name, h_ref in aperiodicas.items():
        error = np.max(np.abs(modified_h(h_name) - h_ref))
        print(f"  {h_name:17s} max|h_etapa4 - h_etapa3| = {error:.1e}")
    print(f"  {'Entrada':17s}{'Respuesta':17s}{'E_sal':>10}{'E_sal_val':>10}{'P_sal':>10}")
    for x_name, x in periodicas.items():
        for h_name in RESPUESTAS:
            _, _, e_total, e_valid, power = output_metrics(x, modified_h(h_name))
            print(f"  {x_name:17s}{h_name:17s}{e_total:10.5f}{e_valid:10.5f}{power:10.6f}")


def scaling_rows():
    """Paso 2: h2(t) = a*h(t). Se espera y2 = a*y, y E y P multiplicadas por a^2."""
    rows = []
    for x_name, x in periodicas.items():
        for h_name in RESPUESTAS:
            _, y, e_total, e_valid, power = output_metrics(x, modified_h(h_name))
            for a in A_VALUES:
                _, y2, e2_total, e2_valid, power2 = output_metrics(x, modified_h(h_name, a=a))
                rows.append({
                    "entrada": x_name,
                    "respuesta": h_name,
                    "a": a,
                    "energia_original": e_total,
                    "energia_escalada": e2_total,
                    "energia_valida_original": e_valid,
                    "energia_valida_escalada": e2_valid,
                    "potencia_original": power,
                    "potencia_escalada": power2,
                    "razon_energia": e2_total / e_total,
                    "razon_potencia": power2 / power,
                    "error_max": float(np.max(np.abs(y2 - a * y))),
                })
    return rows


def print_scaling(rows):
    print("Paso 2: escalamiento h2(t) = a*h(t)")
    print(f"  {'Entrada':17s}{'Respuesta':17s}{'a':>5}{'E':>10}{'E2':>10}{'E2/E':>8}"
          f"{'P':>10}{'P2':>10}{'P2/P':>8}{'max|y2-a*y|':>13}")
    for row in rows:
        print(f"  {row['entrada']:17s}{row['respuesta']:17s}{row['a']:5.1f}"
              f"{row['energia_original']:10.5f}{row['energia_escalada']:10.5f}"
              f"{row['razon_energia']:8.4f}{row['potencia_original']:10.6f}"
              f"{row['potencia_escalada']:10.6f}{row['razon_potencia']:8.4f}"
              f"{row['error_max']:13.1e}")
    for a in A_VALUES:
        subset = [row for row in rows if row["a"] == a]
        deviation = max(max(abs(row["razon_energia"] - a**2), abs(row["razon_potencia"] - a**2))
                        for row in subset)
        print(f"  a={a}: a^2={a**2}, mayor desviación de E2/E y P2/P respecto de a^2 = {deviation:.1e}, "
              f"mayor max|y2-a*y| = {max(row['error_max'] for row in subset):.1e}")


def shifting_rows():
    """Paso 3: h3(t) = h(t - t0). Se espera y3(t) = y(t - t0), con E y P iguales.

    La ventana de h no se mueve, así que al desplazar un escalón o una sinc
    cambia el tramo que queda truncado. Por eso se compara dos veces: en todo
    el vector y solo en la zona común no afectada por el truncamiento.
    """
    rows = []
    for x_name, x in periodicas.items():
        for h_name in RESPUESTAS:
            h = modified_h(h_name)
            _, y, e_total, _, power = output_metrics(x, h)
            start, stop, kind = power_window(h)
            valid_start, valid_stop = valid_range(h)
            for t0 in T0_VALUES:
                k = int(round(t0 / dt))                     # corrimiento en muestras
                h3 = modified_h(h_name, t0=t0)
                _, y3 = convolve(x, h3)
                y_shifted = np.r_[np.zeros(k), y[:-k]]      # y(t - t0) en el mismo eje

                # Zona donde ni y3 ni y(t - t0) dependen del tramo truncado de h.
                valid3_start, valid3_stop = valid_range(h3)
                common_start = max(valid3_start, valid_start + k)
                common_stop = min(valid3_stop, valid_stop + k)
                common = slice(common_start, common_stop)

                # Inversión por medio periodo: y(t - T0/2) = -y(t) en régimen.
                inversion = ""
                if kind == "régimen permanente" and np.isclose(t0, T0 / 2):
                    regime = slice(start + k, stop)
                    inversion = float(np.max(np.abs(y3[regime] + y[regime])))

                rows.append({
                    "entrada": x_name,
                    "respuesta": h_name,
                    "t0_s": t0,
                    "area_h_original": float(np.sum(h) * dt),
                    "area_h_desplazada": float(np.sum(h3) * dt),
                    "energia_original": e_total,
                    "energia_desplazada": energy(y3),
                    "energia_comun_original": energy(y_shifted[common]),
                    "energia_comun_desplazada": energy(y3[common]),
                    "potencia_original": power,
                    "potencia_desplazada": mean_power(y3[start + k:stop + k]),
                    "tipo_ventana": kind,
                    "error_max_total": float(np.max(np.abs(y3 - y_shifted))),
                    "error_max_comun": float(np.max(np.abs(y3[common] - y_shifted[common]))),
                    "error_inversion": inversion,
                })
    return rows


def print_shifting(rows):
    print("Paso 3: corrimiento h3(t) = h(t - t0)")
    print(f"  {'Entrada':17s}{'Respuesta':17s}{'t0':>5}{'área h':>8}{'área h3':>8}{'E':>9}{'E3':>9}"
          f"{'Ecom':>9}{'E3com':>9}{'P':>10}{'P3':>10}{'err total':>10}{'err común':>10}{'|y3+y|':>9}")
    for row in rows:
        inversion = row["error_inversion"]
        inversion = f"{inversion:9.1e}" if inversion != "" else f"{'-':>9}"
        print(f"  {row['entrada']:17s}{row['respuesta']:17s}{row['t0_s']:5.2f}"
              f"{row['area_h_original']:8.3f}{row['area_h_desplazada']:8.3f}"
              f"{row['energia_original']:9.5f}{row['energia_desplazada']:9.5f}"
              f"{row['energia_comun_original']:9.5f}{row['energia_comun_desplazada']:9.5f}"
              f"{row['potencia_original']:10.6f}{row['potencia_desplazada']:10.6f}"
              f"{row['error_max_total']:10.1e}{row['error_max_comun']:10.1e}{inversion}")
    print(f"  Mayor error en la zona común: {max(row['error_max_comun'] for row in rows):.1e}")
    print(f"  Mayor |P3 - P|: {max(abs(row['potencia_desplazada'] - row['potencia_original']) for row in rows):.1e}")


def plot_case(number, x_name, x, h_name, h, h_mod, description, tag, shift=0):
    """Figure with the input, both impulse responses and both outputs."""
    t_y, y = convolve(x, h)
    _, y_mod = convolve(x, h_mod)
    start, stop, kind = power_window(h)
    start, stop = start + shift, stop + shift          # la ventana sigue a la salida
    valid_start, valid_stop = valid_range(h_mod)

    fig, axes = plt.subplots(3, 1, figsize=(8.2, 9.2))
    axes[0].plot(t_x, x, color="tab:blue")
    axes[0].set_title(f"Entrada: {x_name}")
    axes[0].set_ylabel("x(t) [u.a.]")
    axes[1].plot(t_h, h, color="tab:orange", label="h(t) original")
    axes[1].plot(t_h, h_mod, color="tab:red", linestyle="--", label=description)
    axes[1].set_title(f"Respuesta a impulso: {h_name}")
    axes[1].set_ylabel("h(t) [1/s]")
    axes[2].plot(t_y, y, color="tab:green", label="y(t) original")
    axes[2].plot(t_y, y_mod, color="tab:purple", linestyle="--", label="y(t) modificada")
    axes[2].set_title("Salidas")
    axes[2].set_ylabel("y(t) [u.a.]")
    axes[2].axvspan(t_y[start], t_y[stop - 1] + dt, color="tab:green", alpha=0.15,
                    label=f"Ventana de potencia ({kind})")
    label = "Afectado por el truncamiento de h(t)"
    if valid_start > 0:
        axes[2].axvspan(t_y[0], t_y[valid_start], color="0.5", alpha=0.25, label=label)
        label = None
    if valid_stop < y.size:
        axes[2].axvspan(t_y[valid_stop], t_y[-1], color="0.5", alpha=0.25, label=label)
    for axis in axes:
        axis.set_xlim(t_y[0], t_y[-1])
        axis.set_xlabel("Tiempo [s]")
        axis.grid(True, alpha=0.3)
    axes[1].legend(loc="upper right", fontsize=8)
    axes[2].legend(loc="upper right", fontsize=8)
    fig.suptitle(f"Figura {number}: {x_name} * {h_name}, {description}")
    fig.tight_layout()
    path = FIG_DIR / f"fig{number:02d}_{slug(x_name)}_{slug(h_name)}_{tag}.pdf"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def make_figures():
    """Paso 4: una figura por entrada graficada, sistema y modificación."""
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    number = FIRST_FIGURE_4
    for x_name in FIGURE_INPUTS:
        x = periodicas[x_name]
        for h_name in RESPUESTAS:
            h = modified_h(h_name)
            for a in A_VALUES:
                tag = f"a_{a:g}".replace("-", "m").replace(".", "p")
                plot_case(number, x_name, x, h_name, h, modified_h(h_name, a=a),
                          f"$h_2(t) = {a:g}\\,h(t)$", tag)
                number += 1
            for t0 in T0_VALUES:
                tag = f"t0_{int(round(t0 * 1000))}ms"
                plot_case(number, x_name, x, h_name, h, modified_h(h_name, t0=t0),
                          f"$h_3(t) = h(t - {t0:g}\\,\\mathrm{{s}})$", tag,
                          shift=int(round(t0 / dt)))
                number += 1
    print(f"Paso 4: figuras {FIRST_FIGURE_4} a {number - 1} guardadas en {FIG_DIR}")


def summary_rows(scaling, shifting):
    """Paso 5: one row per case with E and P of the original and modified outputs."""
    summary = {}
    for row in scaling:
        entry = summary.setdefault((row["entrada"], row["respuesta"]), {
            "entrada": row["entrada"],
            "respuesta": row["respuesta"],
            "E_original": row["energia_original"],
            "P_original": row["potencia_original"],
        })
        entry[f"E_a={row['a']:g}"] = row["energia_escalada"]
        entry[f"P_a={row['a']:g}"] = row["potencia_escalada"]
    for row in shifting:
        entry = summary[(row["entrada"], row["respuesta"])]
        entry[f"E_t0={row['t0_s']:g}s"] = row["energia_desplazada"]
        entry[f"P_t0={row['t0_s']:g}s"] = row["potencia_desplazada"]
    for row in shifting:                    # al final, para que quede como última columna
        summary[(row["entrada"], row["respuesta"])]["tipo_ventana"] = row["tipo_ventana"]
    return list(summary.values())


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Tabla guardada en {path}")


def print_summary(rows):
    print("Paso 5: resumen de energía (E) y potencia media (P) de la salida")
    for prefix, fmt in (("E", "10.5f"), ("P", "10.6f")):
        keys = [key for key in rows[0] if key.startswith(prefix + "_")]
        print("  " + f"{'Entrada':17s}{'Respuesta':17s}" + "".join(f"{key:>12s}" for key in keys))
        for row in rows:
            print("  " + f"{row['entrada']:17s}{row['respuesta']:17s}"
                  + "".join(f"{row[key]:>12.{fmt[3:]}}" for key in keys))


def main():
    check_base()
    scaling = scaling_rows()
    shifting = shifting_rows()
    print_scaling(scaling)
    print_shifting(shifting)
    make_figures()
    summary = summary_rows(scaling, shifting)
    print_summary(summary)
    write_csv(CSV_SCALING, scaling)
    write_csv(CSV_SHIFTING, shifting)
    write_csv(CSV_SUMMARY, summary)


if __name__ == "__main__":
    main()
