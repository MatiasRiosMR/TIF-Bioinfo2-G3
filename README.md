# Trabajo Práctico Integrador de Bioinformática 2

<div align="center">
  <img src="./data/logo_fiuner.png" alt="Logo FIUNER" width="200">
</div>

**Asignatura:** Bioinformática 2

**Institución:** Facultad de Ingeniería, Universidad Nacional de Entre Ríos

**Año:** 2026

---

## Introducción

Este repositorio documenta el desarrollo y los resultados de un trabajo práctico integrador orientado al análisis bioinformático de un brote de *Brucella*. La intención es proporcionar una guía reproducible para cada etapa del proyecto, junto con los resultados obtenidos durante el desarrollo.

El proyecto se organiza por actividades, cada una con un objetivo específico dentro del flujo de trabajo genómico:

1. Ensamblado y evaluación de calidad
2. Anotación funcional y búsqueda BLAST
3. Filogenia comparativa
4. Diseño de primers y análisis de sitios de restricción

---

## Equipo Responsable

- Sara Barbara
- Emilia Vergara
- Matías Ríos

---

## Resumen de Actividades

### Actividad 2: Ensamblado y evaluación de calidad

Objetivo: generar un ensamblado híbrido de la secuencia de *Brucella* y evaluar su calidad con métricas estándar.

Contenidos principales:
- `actividad-2-ensamblado/spades_hybrid/`: ejecución de SPAdes para ensamblado híbrido.
- `actividad-2-ensamblado/quast_hybrid/`: reportes de QUAST con estadísticas de ensamblado.
- `secuencia_consenso.fasta` y `Set3.fq`: insumos de secuencias utilizadas.

Resultado: un ensamblado de mayor calidad validado por métricas como N50, longitud total y número de contigs.

### Actividad 4: Anotación funcional y búsqueda BLAST

Objetivo: caracterizar las secuencias ensambladas mediante anotación automática y comparación con bases de datos de proteínas.

Contenidos principales:
- `actividad-4-anotacion/results_prokka/`: anotación funcional realizada con Prokka.
- `actividad-4-anotacion/results_prodigal/`: predicción de genes con Prodigal.
- `actividad-4-anotacion/pipeline-blast_local/`: análisis local de BLAST contra SwissProt.

Resultado: generación de archivos de anotación estructural y funcional, además de identificaciones de homologías significativas.

### Actividad 5: Filogenia comparativa

Objetivo: inferir relaciones filogenéticas con base en alineamientos de secuencias seleccionadas.

Contenidos principales:
- `actividad-5-filogenia/data_secuencias/`: secuencias de referencia utilizadas para el análisis.
- `actividad-5-filogenia/results-msa/Multifasta.aln`: alineamiento múltiple generado.
- `actividad-5-filogenia/data-arbol/ML_clustal.tree`: árbol filogenético resultante.

Resultado: un árbol filogenético que posiciona las secuencias de *Brucella* frente a referencias relevantes.

### Actividad 6: Diseño de primers y análisis de sitios de restricción

Objetivo: diseñar primers específicos para la amplificación de regiones de interés y estudiar sitios de restricción asociados.

Contenidos principales:
- `actividad-6-diseno-primers/diseñar_primers.py`: script principal del pipeline de diseño.
- `actividad-6-diseno-primers/primer_pipeline/`: módulos auxiliares del pipeline.
- `actividad-6-diseno-primers/data/`: datos de entrada, incluida la anotación y el ensamblado.
- `actividad-6-diseno-primers/resultado/`: resultados de primers, productos esperados y mapas de enzimas.

Resultado: conjunto de primers propuestos, sus productos de PCR simulados y el análisis de sitios de restricción.

---

## Requisitos de Software

### Dependencias de Python

- Python 3.8 o superior
- Biopython

Instalación:

```bash
pip install -r requirements.txt
```

### Dependencias de bioinformática opcionales

Para ejecutar localmente las etapas de ensamblado, anotación y BLAST:

- SPAdes
- QUAST
- Prodigal
- Prokka
- BLAST+

Ejemplo con Conda:

```bash
conda create -n tp_bioinfo2 python=3.8
conda activate tp_bioinfo2
conda install -c bioconda spades quast prodigal prokka blast biopython
```

> Nota: los resultados ya generados están almacenados en el repositorio. La reproducibilidad completa requiere actualizar rutas y configurar las bases de datos según el entorno local.

---

## Guía de Reproducción

### Actividad 2: Reproducir ensamblado híbrido

1. Ingresar al directorio:

```bash
cd actividad-2-ensamblado/spades_hybrid/
```

2. Revisar y adaptar `run_spades.sh` para las rutas locales.
3. Ejecutar el script:

```bash
bash run_spades.sh
```

4. Evaluar el ensamblado con QUAST en `actividad-2-ensamblado/quast_hybrid/`.

### Actividad 4: Reproducir anotación y BLAST local

1. Ingresar al directorio de BLAST:

```bash
cd actividad-4-anotacion/pipeline-blast_local/
```

2. Descargar y preparar SwissProt local:

```bash
wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz
gunzip uniprot_sprot.fasta.gz
makeblastdb -in uniprot_sprot.fasta -dbtype prot -out swissprot
```

3. Ajustar la variable `DB` en `blast_analizar_top3hits.sh` con la ruta absoluta del archivo `swissprot`.
4. Ejecutar el análisis:

```bash
bash blast_analizar_top3hits.sh
```

### Actividad 5: Reproducir filogenia

1. Revisar `actividad-5-filogenia/data_secuencias/` y `results-msa/`.
2. Validar los alineamientos con la herramienta de su preferencia.
3. Visualizar el árbol en `actividad-5-filogenia/data-arbol/ML_clustal.tree`.

### Actividad 6: Reproducir diseño de primers

1. Ingresar al directorio:

```bash
cd actividad-6-diseno-primers/
```

2. Ejecutar el script principal:

```bash
python3 diseñar_primers.py -f data/scaffolds.fasta -g data/brucella_hybrid.gff -o resultado
```

3. Consultar los archivos generados en `resultado/`.

---

## Resultados Generados

Los resultados principales ya se encuentran incluidos en el repositorio. Los archivos más relevantes son:

- `actividad-2-ensamblado/quast_hybrid/report.txt`: métricas de calidad del ensamblado.
- `actividad-4-anotacion/results_prokka/brucella_hybrid.gff`: anotación funcional y estructural.
- `actividad-4-anotacion/pipeline-blast_local/blast_swissprot.tsv`: resultados de BLAST local.
- `actividad-5-filogenia/results-msa/Multifasta.aln`: alineamiento múltiple.
- `actividad-5-filogenia/data-arbol/ML_clustal.tree`: árbol de filogenia.
- `actividad-6-diseno-primers/resultado/res_primers.tab`: tabla de primers diseñados.
- `actividad-6-diseno-primers/resultado/res_prod.fa`: secuencias de los productos de PCR.
- `actividad-6-diseno-primers/resultado/res_enzimas.tab`: análisis de sitios de restricción.

---

## Estructura del Repositorio

```text
README.md
requirements.txt
actividad-2-ensamblado/
  ├── secuencia_consenso.fasta
  ├── Set3.fq
  ├── quast_hybrid/
  └── spades_hybrid/
actividad-4-anotacion/
  ├── GCF_genoma_referencia.fna
  ├── scaffolds.fasta
  ├── data-genoma-referencia/
  ├── pipeline-blast_local/
  │   ├── blast_analizar_top3hits.sh
  │   └── db/
  ├── results_prodigal/
  └── results_prokka/
actividad-5-filogenia/
  ├── data_secuencias/
  ├── data-arbol/
  └── results-msa/
actividad-6-diseno-primers/
  ├── diseñar_primers.py
  ├── primer_pipeline/
  ├── data/
  └── resultado/
```

---

## Observaciones de Reproducibilidad

- Algunas rutas dentro de los scripts están configuradas para el entorno original del desarrollo y deben adaptarse en equipos distintos.
- Las bases de datos de BLAST pueden ser voluminosas; se recomienda realizar la descarga en un entorno con conexión estable.
- Los resultados incluidos se ofrecen como referencia para la evaluación, pero el flujo de trabajo completo puede reproducirse con las herramientas listadas.

---

## Licencia y Uso

Este trabajo se presenta con fines académicos. Su uso externo o comercial requiere autorización del equipo responsable y de la institución.

---

## Versión

**v1.0** - Junio 2026
