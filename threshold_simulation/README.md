# Simulación de los umbrales dinámicos

Esta carpeta reproduce numéricamente dos cambios cualitativos del modelo de
Acemoglu, Kong y Ozdaglar (2026):

1. el cruce de `alpha - 1 = 1/4`, equivalente a `alpha = 1.25`; y
2. el cruce de la precisión crítica de la IA `tau_A^c` cuando `alpha = 1.2`,
   que pertenece al régimen elástico (`alpha - 1 < 1/4`).

La simulación es una ilustración del modelo y no sustituye las demostraciones
de los Lemas 1-2 ni de las Proposiciones 3 y 5 del artículo.

## Modelo utilizado

Para una precisión pública `X`, el esfuerzo individual resuelve

```text
e^(alpha-1) = Delta_X lambda_I G(X) g(sigma^(-2) + lambda_I e + tau_A),
```

donde `G(q) = 2 Phi(sqrt(q)) - 1` y
`g(q) = phi(sqrt(q))/sqrt(q)`. La ley de movimiento es

```text
F(X) = (X + lambda_G I e(X,tau_A))
       / (1 + Sigma^2 (X + lambda_G I e(X,tau_A))).
```

Se usan los parámetros de la simulación principal del repositorio:

| Parámetro | Valor |
|---|---:|
| `sigma^(-2)` | 0.5 |
| `lambda_I` | 1 |
| `lambda_G` | 1 |
| `I` | 1000 |
| `Sigma^2` | 1 |
| `Delta_X` | 1 |

## Experimento 1: cruce de `alpha = 1.25`

Se comparan `alpha = 1.20`, `1.25` y `1.30`, con `tau_A = 0`, desde
`X_0 = 0.02` y `X_0 = 0.8`.

- Con `alpha = 1.20`, cero es localmente estable. Para estos parámetros hay
  además un estado inestable que separa la cuenca de colapso de la cuenca del
  estado alto.
- Con `alpha = 1.30`, cero es inestable y toda condición inicial positiva
  converge al único estado positivo.
- La teoría citada en el artículo usa desigualdades estrictas y no clasifica
  `alpha = 1.25`. El panel de igualdad registra únicamente lo que sucede con
  esta parametrización.

El resultado se guarda en `outputs/alpha_crossing.png`.

## Experimento 2: cruce de `tau_A^c`

Se fija `alpha = 1.20` y se calcula `tau_A^c` resolviendo la condición de
tangencia: el máximo de `F(X)-X` sobre los estados positivos es cero. Después
se comparan `0.75 tau_A^c`, `tau_A^c` y `1.25 tau_A^c`.

- Debajo del umbral aparecen dos estados positivos: uno inestable y otro
  estable.
- En el umbral ambos estados se unen en una raíz doble. Desde arriba, las
  trayectorias se aproximan a la tangencia; desde abajo, se alejan hacia cero.
- Encima del umbral no queda ningún estado positivo y todas las trayectorias
  simuladas convergen hacia cero.

El resultado se guarda en `outputs/tau_crossing.png`. El archivo
`outputs/bifurcation_diagrams.png` resume cómo cambian los puntos fijos en ambos
experimentos. Los valores numéricos y las comprobaciones se guardan en
`outputs/results.json`.

## Ejecución

Desde la raíz del repositorio:

```sh
python threshold_simulation/simulate_thresholds.py
```

Para escribir los resultados en otro directorio:

```sh
python threshold_simulation/simulate_thresholds.py --out ruta/de/salida
```

Dependencias: `numpy`, `scipy` y `matplotlib`; están enumeradas en
`requirements.txt`.
