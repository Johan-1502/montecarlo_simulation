# Random Numbers Library

Este repositorio implementa una librería en Python para la generación de números pseudoaleatorios y la evaluación de su aleatoriedad mediante pruebas estadísticas. Está pensada para ser usada como módulo importable en otros proyectos.

## Project Structure

```
random-numbers-library/
│
├── distributions/
│   ├── Distributions.py              # Distribuciones
│   ├── ExponentialDistribution.py
│
├── generators/
│   ├── Congruences.py
│   ├── HalfSquares.py
│   └── test/
│       └── RandomTest.py             # pruebas
│
├── Random.py                         # Clase Fachada
├── RandomUnitTest.py                 # Pruebas simples
└── README.md

```

## Requisitos

Antes de ejecutar el simulador, asegúrate de tener instalado, Python 3.8+ con las siguientes librerias

- numpy
- scipy
  que puede instalar con el siguiente comando

```
pip install numpy scipy
```

## Instalacion

En la consola de comandos

1. Clona el repositorio:

   ```bash
   git clone https://github.com/sunflowerjuan/random-numbers-library

   ```

2. Ingresa al directorio del proyecto:

   ```bash
   cd random-numbers-library
   ```

3. Ejecutar el archivo de pruebas

   ```bash
   python RandomUnitTest.py
   ```

## Random — Generador y Validador de Números Pseudoaleatorios

Este módulo implementa una **fachada** para generación de números pseudoaleatorios, transformación a distribuciones y validación estadística de secuencias.  
Centraliza el uso de un **Congruencial Lineal (LCG)**, distribuciones (uniforme, normal) y pruebas estadísticas para verificar la calidad de los números generados.

---

### Funcionalidades principales

- **Generación de Ri con LCG (LinealCongruence)**

  - Genera números pseudoaleatorios uniformes en `[0,1)`.
  - Control de semilla: **determinista** (reproducible) o **dinámico** (no repetible).

- **Distribuciones**

  - **Uniforme `[a, b]`** (enteros o flotantes).
  - **Normal `N(μ, σ²)`** (Box-Muller transform).

- **Validación estadística automática**

  - Cada secuencia generada se valida con pruebas estadísticas:
    - Media
    - Varianza
    - Chi-Cuadrado
    - Kolmogorov-Smirnov
    - Poker
    - Corridas (Runs)
  - Si una secuencia no pasa, se regenera automáticamente con otra semilla.

- **Extras**
  - `choice(seq)`: selecciona un elemento aleatorio de una lista Validada.

---

## Clase `Random`

La clase `Random` es la **interfaz de alto nivel** para el usuario.  
Internamente combina:

- `LinealCongruence` → generación base de Ri.
- `UniformDistribution` y `NormalDistribution` → transformación de Ri a otras distribuciones.
- `RandomTestFacade` → ejecución de pruebas estadísticas.

### Parámetros del constructor

El constructor por defecto asigba

```python
Random(error=0.05, deterministic=False)
```

### Generador de Congruencias Lineales

```python
lcg = LinealCongruence(xo_seed=seed, k=551757622, c=12345, g=31)
```

Con los valores:

- **m = 2^31 = 2,147,483,648**  
  Se eligió este módulo porque:

  - Es lo suficientemente grande para garantizar secuencias largas antes de repetirse.
  - Se ajusta a enteros de 32 bits, optimizando eficiencia.
  - Es un estándar en muchos LCG conocidos.

- **a = 551757622 (multiplicador)**

  - Escogido para cumplir las condiciones del teorema de **Hull-Dobell** (período máximo).
  - Alejado de múltiplos triviales de `m` para reducir patrones y correlaciones.
  - Proporciona buena dispersión en [0,1).

- **c = 12345 (incremento)**

  - Asegura, junto con `m`, la posibilidad de alcanzar el **período completo**.

- **X₀ = semilla inicial**
  - **Modo dinámico (por defecto):** la semilla se calcula con `time.time_ns()`, generando secuencias distintas en cada ejecución.\_

## License

This project is licensed under the MIT
