# Análisis de resultados

## 1. Efecto de cada sistema sobre las entradas periódicas

Un sistema LTI responde a una exponencial compleja e^{jωt} con la misma exponencial multiplicada por H(jω), la transformada de Fourier de h(t) (Oppenheim et al., 1998, cap. 3). Como las entradas son periódicas con f0 = 2 Hz, cada armónico k·f0 de la entrada queda multiplicado por H(jkω0), con ω0 = 4π rad/s. La Figura 53 muestra |H(f)| para los cinco sistemas, calculada a partir de las mismas h(t) muestreadas que se usaron en las convoluciones.

**Impulso.** H(jω) = 1 en todas las frecuencias, por lo que la salida reproduce la entrada sin cambios (Figuras 5, 10, 15 y 20): el error máximo entre y(t) y x(t) es 1,1·10⁻¹⁶. Es el sistema identidad, y por eso conserva la energía y la potencia.

**Exponencial decreciente.** Su respuesta en frecuencia es H(jω) = (1 − e^{−(1+jω)})/(1 + jω). Como h(t) dura 1 s, que equivale a dos periodos de la entrada, se cumple e^{−jkω0} = 1 y en los armónicos queda H(jkω0) = (1 − e^{−1})/(1 + jkω0). Para kω0 ≫ 1 esto se aproxima a (1 − e^{−1})/(jkω0): el sistema actúa como un integrador escalado, que atenúa cada armónico en proporción a 1/k y lo desfasa cerca de −90°. Por eso la senoidal sale con amplitud 0,0502 y desfase de −85°, y la cuadrada sale con forma casi triangular (Figura 8).

**Exponencial creciente.** De forma análoga, H(jkω0) = (e − 1)/(1 − jkω0) ≈ −(e − 1)/(jkω0): también integra, pero con ganancia mayor (e − 1 = 1,718 frente a 0,632) y con el signo invertido. La senoidal sale con amplitud 0,136 y desfase de +86°, y en régimen permanente las salidas de ambas exponenciales tienen forma casi opuesta (correlación de −0,99 en las cuatro entradas).

**Escalón.** La convolución con u(t) da y(t) = ∫x(τ)dτ desde −∞ hasta t, es decir, la integral acumulada de la entrada. Para la senoidal se obtiene (1 − cos ω0t)/ω0, que oscila entre 0 y 0,159 con valor medio 1/ω0 = 0,0796 (Figura 6), y la cuadrada se transforma en una triangular (Figura 11). Al terminar la entrada (t = 2 s), la salida queda constante en el área total de la entrada, que es prácticamente nula en estas señales de media cero.

**Sinc.** La sinc ideal sen(t)/t corresponde a un filtro pasabajos ideal con ganancia π para |ω| < 1 rad/s (0,16 Hz) y cero fuera de esa banda (Oppenheim et al., 1998, cap. 4). Todos los armónicos de las entradas están en 2 Hz o más, por lo que el filtro los elimina. Lo que aparece entre 1 y 3 s (Figura 7) es el contenido de baja frecuencia producido por el inicio y el fin del tramo de 2 s de entrada, con un máximo de 0,064 para la senoidal; en ese intervalo la salida coincide con la del filtro ideal con un error de 10⁻¹¹.

## 2. Energía y potencia media

Las potencias de entrada coinciden con los valores teóricos de cada forma de onda: A²/2 = 0,5 para la senoidal, A² = 1 para la cuadrada y A²/3 = 0,333 para la triangular y el diente de sierra. La energía en los 2 s de la ventana es el doble de esas potencias.

La potencia de salida se calculó sobre un número entero de periodos y solo donde h(t) se superpone completamente con la entrada (régimen permanente), porque al dividir la energía por toda la duración de la salida se incluyen tramos nulos y transitorios. Con ese criterio se cumple la relación de Parseval P_y = Σ|c_k|²·|H(jkω0)|², que para la senoidal se reduce a P_y = |H(jω0)|²/2: 0,05017²/2 = 0,001258 para la exponencial decreciente y 0,13624²/2 = 0,009280 para la creciente, iguales a los valores medidos. Como todos los sistemas salvo el impulso tienen |H(jkω0)| ≪ 1, la potencia de salida es entre 38 y 37 000 veces menor que la de entrada.

En el escalón y la sinc no existe régimen permanente, porque sus h(t) duran 3 y 4 s, más que los 2 s de la entrada; su potencia se informa sobre una ventana transitoria. Además, el truncamiento del escalón en t = 3 s convierte el sistema en y(t) = ∫x(τ)dτ entre t − 3 y t, que a partir de t = 3 s resta la integral ya acumulada y genera una réplica invertida de la salida (zona gris de la Figura 6). Esa réplica concentra cerca del 50 % de la energía total, por lo que se informa también la energía de la zona no afectada. En la Figura 53 se ve el mismo efecto en frecuencia: una ventana rectangular de 3 s tiene ceros en todos los múltiplos de 1/3 Hz, que incluyen todos los armónicos de 2 Hz.

## 3. Escalamiento y corrimiento de la respuesta a impulso

**Escalamiento.** Con h₂(t) = a·h(t), la constante sale de la integral y la salida es y₂ = a·y. La amplitud se escala por a y la energía y la potencia por a², porque ambas dependen de |y|². Se verificó con a = 2, 0,5 y −1 en las 20 combinaciones: las razones E₂/E y P₂/P valen exactamente 4, 0,25 y 1, y el error entre y₂ y a·y es 0 (multiplicar por esos factores es exacto en punto flotante). Con a = −1 la salida se invierte sin cambiar su energía ni su potencia.

**Corrimiento.** Con h₃(t) = h(t − t0), el sistema equivale a un retardo en cascada con el sistema original, por lo que y₃(t) = y(t − t0): la salida se desplaza sin cambiar de forma, energía ni potencia. Con t0 = 0,1 s y 0,25 s, el error máximo fue de 3,3·10⁻¹⁶ en la zona no afectada por el truncamiento, y la potencia no cambió en ningún caso. En el escalón y la sinc la diferencia sobre todo el vector llega a 0,25, porque la ventana de muestreo [−1, 3) s es fija y al desplazar h(t) cambia la parte que queda fuera: el área del escalón baja de 3 a 2,9 y 2,75, y la de la sinc sube de 2,795 a 2,871 y 2,972. Esto no contradice la invariancia en el tiempo, porque es una diferencia entre dos respuestas a impulso distintas, no un cambio del sistema.

El corrimiento de medio periodo (t0 = T0/2 = 0,25 s) invierte la salida en régimen de la senoidal, la cuadrada y la triangular (error de 10⁻¹⁵), porque esas señales tienen simetría de media onda, x(t − T0/2) = −x(t), al contener solo armónicos impares. El diente de sierra contiene también armónicos pares, que no cambian de signo con ese desplazamiento, y su salida no se invierte (diferencia de hasta 1,0). Para las tres primeras, retrasar T0/2 equivale a escalar por a = −1.

## 4. Conmutatividad

En las cinco combinaciones de señales aperiódicas, A∗B y B∗A coinciden con un error máximo de 8,9·10⁻¹⁶ (Figuras 48 a 52). La propiedad se demuestra con el cambio de variable τ → t − τ en la integral de convolución, e implica que la entrada y la respuesta a impulso pueden intercambiar sus papeles sin cambiar la salida.

Las salidas coinciden con sus expresiones analíticas:
- Exponencial decreciente con creciente: sinh(t) para 0 ≤ t < 1 y sinh(2 − t) para 1 ≤ t < 2, con máximo sinh(1) = 1,1752.
- Exponencial decreciente con escalón: 1 − e^{−t}, que se estabiliza en 0,632, la ganancia DC de la exponencial.
- Impulso con sinc: la propia sinc, con la misma energía (2,31574).
- Escalón con sinc: la integral acumulada de la sinc, Si(t) + Si(1), con máximo 2,5515 en t = 2 s. Frente al caso ideal le falta una constante π/2 − Si(1) ≈ 0,625, que corresponde al área de la sinc anterior a t = −1 s.

La energía del impulso discreto es 1000 = 1/dt, porque se representa con una muestra de altura 1/dt; el impulso ideal tiene energía infinita, por lo que este valor depende del paso de muestreo.

## 5. ¿Son sistemas LTI?

Todos los sistemas del laboratorio se definen como y(t) = ∫x(τ)h(t − τ)dτ con una h(t) fija:
- **Linealidad:** al sustituir αx₁ + βx₂ en la integral se obtiene αy₁ + βy₂, por la linealidad de la integral.
- **Invariancia en el tiempo:** al sustituir x(t − t0) y cambiar la variable a σ = τ − t0 se obtiene y(t − t0), porque h no depende del instante de aplicación.

Por lo tanto, los cinco sistemas originales (usados también en la etapa 5, con los papeles intercambiados) y los 25 sistemas modificados de la etapa 4 son LTI (Haykin y Van Veen, 2001, cap. 2). La verificación numérica lo confirma: los errores de aditividad, homogeneidad e invariancia son menores que 2·10⁻¹⁵ en todos los casos.

Ser LTI no implica otras propiedades:
- **Causalidad:** las exponenciales, el impulso y el escalón son causales (h(t) = 0 para t < 0); la sinc no lo es.
- **Estabilidad BIBO:** el escalón ideal no es estable, porque ∫|u(t)|dt diverge; la sinc ideal tampoco, porque ∫|sen(t)/t|dt diverge. Sus versiones truncadas sí son estables, al tener área absoluta finita (3 y 2,795).

## 6. Limitaciones de la implementación numérica

- **Impulso:** se aproxima con una sola muestra de altura 1/dt. Reproduce exactamente x∗δ = x, pero su energía no es la del impulso ideal.
- **Truncamiento:** el escalón y la sinc se cortan en la ventana [−1, 3) s, lo que genera artefactos que se identificaron y sombrearon en todas las figuras.
- **Duración finita de las entradas:** los 2 s de entrada producen transitorios de inicio y fin. En el escalón y la sinc impiden alcanzar el régimen permanente.
- **Discretización:** la integral se aproxima con una suma de Riemann de paso dt = 1 ms, con un error del orden de dt. Por ejemplo, el área de la exponencial decreciente es 0,63244 frente al valor exacto 0,63212, y su desfase en 2 Hz es −85,09° frente a −85,45°.

## Referencias

- Haykin, S. y Van Veen, B. (2001). *Señales y sistemas*. Limusa Wiley.
- Lathi, B. P. (2005). *Linear Systems and Signals* (2.ª ed.). Oxford University Press.
- Oppenheim, A. V., Willsky, A. S. y Nawab, S. H. (1998). *Señales y sistemas* (2.ª ed.). Prentice Hall.
