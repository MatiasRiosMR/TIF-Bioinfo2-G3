# Proyecto: Bioinformática Aplicada a un Brote de Brucelosis

<div align="center">
  <img src="./data/logo_fiuner.png" alt="Logo FIUNER" width="200">
</div>

**Asignatura:** Bioinformática 2

**Institución:** Facultad de Ingeniería - Universidad Nacional de Entre Ríos

---

## Descripción General

Trabajo Práctico Integrador que presenta un análisis bioinformático completo para un brote de **Brucelosis**. El repositorio contiene resultados y scripts asociados a tres etapas principales:

1. Ensamblado y evaluación de calidad
2. Anotación funcional y búsqueda BLAST
3. Diseño de primers y análisis de sitios de restricción

---

## Estudiantes Responsables

- **Sara Barbara**
- **Emilia Vergara**
- **Matias Rios**

---

## Contenido del Repositorio

- **actividad-2-ensamblado/**: resultados de ensamblado híbrido con SPAdes y evaluación QUAST
- **actividad-4-anotacion/**: resultados de anotación con Prokka/Prodigal y pipeline BLAST local
- **actividad-5-filogenia/**: resultados de alineamiento y árbol filogenético
- **actividad-6-diseno-primers/**: pipeline Python para diseño automático de primers y análisis de restricción

---

## Requisitos

### Dependencias Python

- Python 3.8 o superior
- `biopython>=1.87`

```bash
pip install -r requirements.txt
```

### Dependencias bioinformáticas opcionales

Para reproducir las etapas de ensamblado y anotación fuera de los resultados ya generados:

- `spades`
- `quast`
- `prodigal`
- `prokka`
- `blast+`

Se recomienda instalar estas herramientas con `conda`/`mamba`:

```bash
conda create -n brucelosis-tp python=3.8
conda activate brucelosis-tp
conda install -c bioconda spades quast prodigal prokka blast biopython
```

---

## Uso de los Pipelines

### Diseño de primers (pipeline Python)

El pipeline Python se encuentra en `actividad-6-diseno-primers/diseñar_primers.py`.

```bash
cd actividad-6-diseno-primers/
python3 diseñar_primers.py -f data/scaffolds.fasta -g data/brucella_hybrid.gff -o resultado
```

Archivos de salida esperados:

- `resultado/res_primers.tab`
- `resultado/res_prod.fa`
- `resultado/res_enzimas.tab`
- `resultado/pipeline.stdout.log`
- `resultado/pipeline.stderr.log`

### Ensamblado de genoma (SPAdes)

```bash
cd actividad-2-ensamblado/spades_hybrid/
bash run_spades.sh
```

> Nota: `run_spades.sh` contiene rutas absolutas de un entorno previo y debe ajustarse antes de ejecutarlo.

### Anotación BLAST local

Este proyecto usa una base de datos SwissProt local descargada previamente, ya que la ejecución remota puede demorar mucho y depende de la disponibilidad del servidor NCBI.

```bash
cd actividad-4-anotacion/pipeline-blast_local/
```

#### Descargar SwissProt localmente

```bash
cd actividad-4-anotacion/pipeline-blast_local/db/
wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz
gunzip uniprot_sprot.fasta.gz
makeblastdb -in uniprot_sprot.fasta -dbtype prot -out swissprot
```

#### Modificar el script `blast_analizar_top3hits.sh`

En el script, coloca la ruta completa de la base de datos local en la variable `DB`:

```bash
DB="/ruta/completa/a/actividad-4-anotacion/pipeline-blast_local/db/swissprot"
```

Entonces ejecuta:

```bash
bash blast_analizar_top3hits.sh
```

> Nota: `blast_analizar_top3hits.sh` también requiere que `blastp` esté en el `PATH`.

---

## Estructura del Proyecto

```
TIF-Bioinfo2-G3/
├── README.md
├── requirements.txt
├── actividad-2-ensamblado/
│   ├── secuencia_consenso.fasta
│   ├── Set3.fq
│   ├── quast_hybrid/
│   └── spades_hybrid/
├── actividad-4-anotacion/
│   ├── results_prodigal/
│   ├── results_prokka/
│   └── pipeline-blast_local/
│       └── db/
├── actividad-5-filogenia/
│   ├── data_secuencias/
│   ├── data-arbol/
│   └── results-msa/
└── actividad-6-diseno-primers/
    ├── data/
    ├── diseñar_primers.py
    ├── primer_pipeline/
    ├── res_primers.tab
    ├── res_prod.fa
    └── res_enzimas.tab
```

---

## Resultados disponibles

- `actividad-2-ensamblado/quast_hybrid/`: reportes de calidad de ensamblado
- `actividad-4-anotacion/results_prokka/`: anotación funcional con Prokka
- `actividad-4-anotacion/pipeline-blast_local/blast_swissprot.tsv`: resultados BLAST
- `actividad-6-diseno-primers/res_primers.tab`: tabla de primers diseñados
- `actividad-6-diseno-primers/res_prod.fa`: productos de PCR en formato FASTA
- `actividad-6-diseno-primers/res_enzimas.tab`: análisis de sitios de restricción

---

## Notas importantes

- El pipeline Python de diseño de primers requiere solo `biopython` como dependencia externa.
- Los scripts de ensamblado y BLAST incluyen rutas fijas que deben actualizarse para ejecutarse en otro equipo.
- El proyecto está diseñado para Linux/Unix.

---

## Versión

**v1.0** - Junio 2026

---

## Licencia

Uso académico únicamente. Solicitar autorización para uso externo.
