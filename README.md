# Proyecto: Bioinformática Aplicada a un Brote de Brucelosis

![Logo Facultad](./data/logo_fiuner.png)

**Asignatura:** Bioinformática 2

**Institución:** Facultad de Ingeniería - Universidad Nacional de Entre Ríos

---

## Descripción General

Trabajo Práctico Integrador que implementa un pipeline bioinformático completo para el análisis y anotación de genomas bacterianos aplicado al estudio de un brote de **Brucelosis**. El proyecto integra múltiples etapas: ensamblado de secuencias, análisis de calidad, anotación funcional, análisis filogenético y diseño de primers.

---

## Estudiantes Responsables

- **Sara Barbara**
- **Emilia Vergara**  
- **Matias Rios**

---

## Contenido del Repositorio

Este repositorio contiene todos los scripts, configuraciones y documentos con resultados utilizados para el desarrollo del trabajo práctico:

- **actividad-2-ensamblado/**: Scripts y resultados del ensamblado híbrido de lecturas cortas y largas usando SPAdes, incluyendo reportes de calidad (QUAST)

- **actividad-4-anotacion/**: Predicción de genes (Prodigal) y anotación funcional (Prokka). Refinamiento mediante búsquedas BLAST contra la base de datos SwissProt. Incluye script automatizado para paralelizar búsquedas y tabla consolidada con funciones predichas

- **actividad-5-filogenia/**: Análisis evolutivo de *Brucella suis* mediante PSI-BLAST, alineamiento múltiple (Clustal X), identificación de dominios conservados (InterPro) y construcción de árbol filogenético para comparar con otras especies bacterianas

- **actividad-6-diseno-primers/**: Pipeline en Python/bash que diseña primers específicos de 20 nucleótidos para cada gen. Calcula temperaturas de melting (Tm) y annealing (Ta), genera productos de PCR en FASTA, y analiza sitios de restricción (EcoRI, BamHI, AvaII) para evaluación de clonado

---

## Requisitos e Instalación

### Dependencias de Software

Este proyecto requiere las siguientes herramientas bioinformáticas:

- **SPAdes** - Ensamblador híbrido de genomas
- **QUAST** - Herramienta de evaluación de calidad de ensamblados
- **Prodigal** - Predictor de genes procariotes
- **Prokka** - Anotador rápido de genomas bacterianos
- **BLAST+** - Herramienta de búsqueda de similitud de secuencias
- **BioPython** - Librería Python para bioinformática

### Instalación de Dependencias Python

1. **Clonar o descargar el repositorio**:
   ```bash
   git clone <url-repositorio>
   cd TIF-Bioinfo2-G3
   ```

2. **Instalar dependencias Python**:
   ```bash
   pip install -r requirements.txt
   ```

### Herramientas Bioinformáticas Recomendadas

Se recomienda usar conda/mamba para instalar las herramientas bioinformáticas:

```bash
# Crear ambiente conda
conda create -n brucelosis-tp python=3.8

# Activar ambiente
conda activate brucelosis-tp

# Instalar herramientas
conda install -c bioconda spades quast prodigal prokka blast biopython
```

---

## Configuración del Pipeline de Anotación

### Opción 1: Base de Datos SwissProt Local (Recomendado)

#### Descargar la Base de Datos SwissProt

```bash
# Descargar SwissProt
cd actividad-4-anotacion/pipeline-blast_local/db/
wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz
gunzip uniprot_sprot.fasta.gz

# Crear índice BLAST
makeblastdb -in uniprot_sprot.fasta -dbtype prot -out swissprot
```

#### Configurar la Ruta en el Script

Edita el archivo `actividad-4-anotacion/pipeline-blast_local/blast_analizar_top3hits.sh` y modifica la variable `DB` con la ruta donde descargaste la base de datos:

```bash
# Línea a modificar en el script:
DB="/ruta/a/tu/base/de/datos/swissprot"
```

### Opción 2: Base de Datos SwissProt Remota

Para usar la base de datos remota de BLAST (NCBI), modifica los parámetros en `blast_analizar_top3hits.sh`:

```bash
# Cambia la base de datos de local a remota
# Comenta la línea local y usa:
blastx -query $INPUT -db swissprot -remote -evalue $EVALUE -num_alignments $MAX_TARGETS -num_threads $THREADS -out $OUTPUT -outfmt 6
```

---

## Estructura del Proyecto

```
TIF-Bioinfo2-G3/
├── README.md                          # Este archivo
├── requirements.txt                   # Dependencias Python
├── actividad-2-ensamblado/           # Ensamblado de genomas
│   ├── secuencia_consenso.fasta
│   ├── Set3.fq
│   ├── quast_hybrid/                 # Resultados de evaluación de calidad
│   └── spades_hybrid/                # Resultados del ensamblado SPAdes
├── actividad-4-anotacion/            # Anotación funcional
│   ├── results_prodigal/             # Resultados de predicción de genes
│   ├── results_prokka/               # Resultados de anotación Prokka
│   └── pipeline-blast_local/         # Pipeline BLAST local
│       └── db/                       # Base de datos BLAST
├── actividad-5-filogenia/            # Análisis filogenético
└── actividad-6-diseno-primers/       # Diseño de primers
    ├── main.py
    ├── requirements.txt
    ├── primer_pipeline/
    └── resultado/
```

---

## Uso de los Pipelines

### 1. Ensamblado (SPAdes)

```bash
cd actividad-2-ensamblado/
bash run_spades.sh
```

### 2. Anotación (BLAST Local)

```bash
cd actividad-4-anotacion/pipeline-blast_local/
# Asegúrate de haber configurado la ruta DB correctamente
bash blast_analizar_top3hits.sh
```

### 3. Diseño de Primers

```bash
cd actividad-6-diseno-primers/
python main.py
```

---

## Datos Utilizados

Los datos utilizados en este trabajo práctico fueron proporcionados por la **Cátedra de Bioinformática 2** de la Facultad de Ingeniería (UNER) para el análisis y estudio del brote de brucelosis porcina.

---

## Resultados

Todos los resultados generados durante el análisis se encuentran organizados en sus respectivas carpetas:

- **Reportes de Calidad**: `actividad-2-ensamblado/quast_hybrid/`
- **Anotación de Genes**: `actividad-4-anotacion/results_prokka/`
- **Resultados BLAST**: `actividad-4-anotacion/pipeline-blast_local/blast_swissprot.tsv`
- **Primers Diseñados**: `actividad-6-diseno-primers/resultado/`

---

## Autorización para Reproducción

Este trabajo y todos sus contenidos (scripts, datos, análisis y resultados) se comparten **exclusivamente con fines educativos y de investigación académica**.

**Se solicita autorización previa** para:
- Reproducción total o parcial del análisis
- Reutilización de los scripts en otros proyectos
- Publicación o presentación de los resultados
- Distribución del código o datos

Para obtener autorización, contactar a:
- Sara Barbara
- Emilia Vergara
- Matias Rios

---

## Notas Importantes

- Los scripts contienen rutas específicas que pueden necesitar ajustes según tu entorno
- Se recomienda ejecutar los pipelines en un sistema Linux/Unix
- Asegúrate de tener suficiente espacio en disco para las bases de datos y resultados
- La ejecución completa del pipeline puede requerir varias horas

---

## Versión

**v1.0** - Junio 2026

---

## Licencia

Este proyecto es de uso restringido. Se debe solicitar autorización para cualquier uso fuera del ámbito académico.
