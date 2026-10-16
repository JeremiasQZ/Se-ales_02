# Laboratorio 2: Sistemas LTI y Convolución

Código y resultados de la Experiencia 2 del Laboratorio de Señales y Sistemas.
Cada etapa de la guía tiene su propio script en la raíz y su propia carpeta
dentro de `resultados/`.

## Estructura

```
Señales.py          Etapas 1 y 2: parámetros y definición de las señales
etapa1_2.py         Etapas 1 y 2: gráficos de las señales
etapa3.py           Etapa 3: convolución de las 4 entradas con las 5 respuestas
etapa4.py           Etapa 4: escalamiento y corrimiento de las respuestas
etapa5.py           Etapa 5: conmutatividad con señales aperiódicas
etapa6.py           Etapa 6: respuesta en frecuencia, como apoyo al análisis
resultados/
  etapa1_2/         Figuras 1 y 2
  etapa3/           Tabla CSV y figuras/ (Figuras 3 a 22)
  etapa4/           Tablas CSV y figuras/ (Figuras 23 a 47)
  etapa5/           Tabla CSV y figuras/ (Figuras 48 a 52)
  etapa6/           Figura 53, tabla CSV y analisis_resultados.md
```

El texto del análisis (etapa 6) está en `resultados/etapa6/analisis_resultados.md`.

## Cómo ejecutar

Requiere Python 3 con `numpy`, `scipy` y `matplotlib`. Desde la raíz del repositorio:

```bash
python etapa1_2.py
python etapa3.py
python etapa4.py
python etapa5.py
python etapa6.py
```

Cada script vuelve a generar sus figuras y tablas en `resultados/`. Los scripts
se pueden ejecutar en cualquier orden; `etapa4.py` y `etapa5.py` reutilizan
funciones de `etapa3.py`, pero no necesitan que se haya ejecutado antes.

## Qué hace cada etapa

| Etapa | Script | Qué calcula | Salidas |
|---|---|---|---|
| 1 y 2 | `Señales.py`, `etapa1_2.py` | Cuatro señales periódicas (senoidal, cuadrada, triangular, diente de sierra) y cinco aperiódicas (exponencial decreciente, exponencial creciente, impulso, escalón, sinc) | `fig01_periodicas.pdf`, `fig02_aperiodicas.pdf` |
| 3 | `etapa3.py` | Las 20 convoluciones, energía y potencia de entrada y salida, y verificación numérica de aditividad, homogeneidad e invariancia en el tiempo | `resultados_etapa3.csv` y 20 figuras |
| 4 | `etapa4.py` | Efecto de `a·h(t)` con a = 2, 0,5 y −1, y de `h(t − t0)` con t0 = 0,1 s y 0,25 s | Tres tablas CSV y 25 figuras |
| 5 | `etapa5.py` | Cinco combinaciones de señales aperiódicas intercambiando entrada y respuesta a impulso: conmutatividad, energía, potencia, verificación LTI y zona no afectada por el truncamiento | `resultados_etapa5.csv` y 5 figuras |
| 6 | `etapa6.py` | Respuesta en frecuencia H(jω) de los cinco sistemas, en f0 y sus armónicos, y análisis escrito de todas las etapas | `respuesta_en_frecuencia.csv`, Figura 53 y `analisis_resultados.md` |

## Convenciones

- `fs = 1000 Hz`, `dt = 1/fs`, `f0 = 2 Hz` (`T0 = 0,5 s`), amplitud 1.
- Entradas en `t_x = [0, 2) s` (4 periodos); respuestas a impulso en `t_h = [-1, 3) s`.
- La convolución continua se aproxima con `np.convolve(x, h) * dt`, y el eje de
  la salida es `t_y = t_x[0] + t_h[0] + n·dt`.
- Energía: `E = Σ|x|²·dt`. Potencia media: energía dividida por la duración de
  la ventana, siempre sobre un número entero de periodos.
- La potencia de salida se mide en régimen permanente cuando existe
  (exponenciales e impulso). Para el escalón y la sinc, que duran más que la
  entrada, se mide en una ventana transitoria y así se indica en las tablas.
- Las figuras sombrean en gris las zonas de la salida afectadas por haber
  truncado `h(t)` a la ventana `t_h`.
- Todas las figuras son PDF vectoriales.
