<div align="center">

# Pipeline de Diseño de Primers para *Brucella suis*

<img src="data/logo-fiuner.png" alt="Logo FIUNER" width="180">

## Trabajo Final Integrador

### Bioinformática 2

**Licenciatura en Bioinformática**
**Facultad de Ingeniería – Universidad Nacional de Entre Ríos**

---

### Integrantes

**Barbara Sara**
**Emilia Vergara**
**Matías Ríos**

### Docentes

**Ileana Tossolini**
**Juan Manuel Cabrera**

</div>

---

# Descripción del Proyecto

El equipo de profesionales a cargo del proyecto tiene como objetivo desarrollar un kit diagnóstico basado en PCR para detectar *Brucella suis*, el agente responsable del reciente brote de brucelosis porcina en Entre Ríos. La técnica de PCR permite una detección rápida y precisa de patógenos a partir de material genético, y se ha utilizado exitosamente en el diagnóstico de enfermedades como tuberculosis, dengue y COVID-19.

En esta etapa del trabajo, el equipo de bioinformáticos debe generar un script en Python que permita diseñar primers específicos para todos los genes predichos en el ensamblado de la cepa responsable del brote. El pipeline toma como entrada la secuencia FASTA resultante del ensamblado y el archivo GFF con los genes predichos, y devuelve primers y productos de PCR listos para análisis.

Este pipeline modular permite diseñar pares de primers, calcular parámetros termodinámicos, generar productos de PCR y realizar análisis de sitios de restricción sobre regiones génicas anotadas.

---

# Objetivos

* Diseñar primers forward y reverse para genes anotados como `CDS`.
* Calcular temperaturas de fusión (**Tm**) y alineamiento (**Ta**).
* Generar amplicones en formato FASTA.
* Analizar sitios de restricción utilizando enzimas seleccionadas.
* Generar reportes tabulados para facilitar la interpretación de resultados.
* Usar como entrada la secuencia FASTA resultante del ensamblado y el archivo GFF de genes predichos.

---

# Estructura del Repositorio

```text
.
├── main.py
├── requirements.txt
├── data/
├── example_data/
│   ├── genoma.fasta
│   └── genes.gff
├── primer_pipeline/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── designer.py
│   └── utils.py
└── primer-pipeline
```

| Archivo / Directorio | Descripción                         |
| -------------------- | ----------------------------------- |
| `main.py`            | Script principal de ejecución       |
| `requirements.txt`   | Dependencias del proyecto           |
| `example_data/`      | Datos de ejemplo                    |
| `data/`              | Directorio de entrada y salida      |
| `primer_pipeline/`   | Implementación modular del pipeline |

---

# Flujo de Trabajo

1. Cargar la secuencia genómica en formato FASTA.
2. Cargar las anotaciones génicas en formato GFF.
3. Filtrar características anotadas como `CDS`.
4. Diseñar primers forward y reverse para cada gen.
5. Calcular parámetros termodinámicos.
6. Generar amplicones en formato FASTA.
7. Analizar sitios de restricción.
8. Generar reportes finales.

---

# Requisitos

* Python 3
* Biopython

## Instalación

```bash
pip install -r requirements.txt
```

Si el archivo `requirements.txt` no estuviera actualizado:

```bash
pip install biopython
```

---

# Uso

El pipeline está pensado para recibir como entrada:

* la secuencia FASTA resultante del ensamblado
* el archivo GFF con los genes predichos

Para ejecutar el pipeline desde la raíz del proyecto con datos de ejemplo de prueba, utilice el siguiente comando:

```bash
python3 main.py -f example_data/genoma.fasta -g example_data/genes.gff -o resultado
```

Este comando carga los datos de ejemplo desde `example_data/` y guarda los resultados en el directorio `resultado`.

> Nota: los archivos dentro de `example_data/` se usan solo como prueba; para el trabajo final se debe usar el ensamblado real y su GFF de genes predichos.

## Parámetros

| Parámetro        | Descripción                             |
| ---------------- | --------------------------------------- |
| `-f`, `--fasta`  | Archivo FASTA con la secuencia genómica |
| `-g`, `--gff`    | Archivo GFF con anotaciones génicas     |
| `-o`, `--output` | Directorio de salida                    |

---

# Resultados Generados

El pipeline genera los siguientes archivos:

| Archivo           | Descripción                                      |
| ----------------- | ------------------------------------------------ |
| `res_primers.tab` | Reporte de primers diseñados                     |
| `res_prod.fa`     | Secuencias de amplicones generados               |
| `res_enzimas.tab` | Resultados del análisis de sitios de restricción |

---

# Alcance

* Procesamiento de genes anotados como `CDS`.
* Diseño de primers básicos de 20 nucleótidos.
* Cálculo de parámetros termodinámicos simples.
* Análisis de un conjunto predefinido de enzimas de restricción.

---

# Tecnologías Utilizadas

* Python
* Biopython
* FASTA
* GFF3

---

# Contexto Académico

Este proyecto fue desarrollado como Trabajo Final Integrador de la asignatura **Bioinformática 2**, correspondiente a la **Licenciatura en Bioinformática** de la **Facultad de Ingeniería de la Universidad Nacional de Entre Ríos (FI-UNER)**.
