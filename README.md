# Pipeline de Diseño de Primers para PCR (Brucella suis)

Breve descripción
-------------------

Proyecto desarrollado como Trabajo Final Integrador de la asignatura *Bioinformática 2* (FI-UNER). El pipeline automatiza el diseño de pares de primers para genes anotados (CDS) a partir de un ensamblado genómico y su archivo de anotaciones GFF, genera amplicones en FASTA y realiza un análisis sencillo de sitios de restricción.

Contenido del repositorio
-------------------------

```text
diseno-primers/
	├── main.py
	├── requirements.txt
	├── example_data/
	│   ├── genes.gff
	│   └── genomas.fna
	├── primer_pipeline/
	│   ├── __init__.py
	│   ├── analyzer.py
	│   ├── designer.py
	│   └── utils.py
resultado/
	├── res_enzimas.tab
	├── res_primers.tab
	└── res_prod.fa
pipeline-blast_local/
	└── blast_analizar_top3hits.sh
``` 

Resumen de componentes
- `diseno-primers/main.py`: CLI que orquesta el pipeline de diseño y análisis.
- `diseno-primers/primer_pipeline/designer.py`: carga FASTA/GFF, genera primers y amplicones.
- `diseno-primers/primer_pipeline/analyzer.py`: detecta sitios de restricción en amplicones.
- `diseno-primers/primer_pipeline/utils.py`: utilidades (reverse complement, IUPAC → regex).
- `pipeline-blast_local/blast_analizar_top3hits.sh`: script Bash para ejecutar BLASTp contra Swiss‑Prot local.

Requisitos
----------

- Sistema: Linux / macOS (se han probado scripts en entornos GNU/Linux).
- Python 3.8+.
- BLAST+ (para uso del script de BLAST local): `blastp`, `makeblastdb`, `blastdbcmd`.
- Dependencias de Python: ver `diseno-primers/requirements.txt` (actualmente `biopython`).

Instalación rápida
------------------

1. Crear y activar un entorno virtual (recomendado):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instalar dependencias de Python:

```bash
pip install -r diseno-primers/requirements.txt
```

3. Instalar BLAST+ (si se usará la búsqueda local):

En Debian/Ubuntu:

```bash
sudo apt update
sudo apt install ncbi-blast+
```

O consulte la documentación de NCBI para otras plataformas.

Configuración y uso del pipeline de diseño de primers
-----------------------------------------------------

Ejemplo de ejecución con datos de ejemplo incluidos:

```bash
cd diseno-primers
python3 main.py -f example_data/genoma.fasta -g example_data/genes.gff -o ../resultado
```

Salida esperada (en `resultado/`):

- `res_primers.tab`: tabla con pares de primers (Tm y Ta calculados) por gen.
- `res_prod.fa`: amplicones (FASTA) generados a partir de las coordenadas GFF.
- `res_enzimas.tab`: resultados del análisis de sitios de restricción.

Notas sobre el diseño de primers
- El diseñador actual selecciona primers de longitud fija (20 nt) tomando los primeros/últimos 20 nt del CDS. La fórmula de Tm implementada es empírica; revise/ajuste según criterios experimentales.

Swiss‑Prot: opción recomendada en este pipeline
---------------------------------------------

Para la etapa de análsis por homología (BLAST), el equipo decidió usar Swiss‑Prot local. Hay dos opciones:

1) Descargar y construir la base de datos Swiss‑Prot local (recomendado si tiene acceso a disco y CPU):

```bash
# crear carpeta para DB
mkdir -p /ruta/a/db/swissprot
cd /ruta/a/db/swissprot

# bajar el FASTA de Swiss-Prot (UniprotKB/Swiss-Prot). URL de ejemplo (actualizar si cambia):
wget -O uniprot_sprot.fasta.gz https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz
gunzip uniprot_sprot.fasta.gz

# construir la DB para BLAST (prefijo 'swissprot')
makeblastdb -in uniprot_sprot.fasta -dbtype prot -out swissprot -title swissprot

# Resultado: archivos swissprot.* en /ruta/a/db/swissprot
```

Después de esto, ajuste la variable `DB` en `pipeline-blast_local/blast_analizar_top3hits.sh` para apuntar al prefijo `/ruta/a/db/swissprot/swissprot` o modifique la variable `DB` al directorio que contenga los archivos de la DB según espera el script.

2) Usar BLAST remoto (sin base de datos local). Si no desea descargar la base completa, puede modificar el script `blast_analizar_top3hits.sh` para usar la opción `-remote` de `blastp`.

Ejemplo de cambio mínimo en el script (concepto):

```bash
# variable nueva al inicio del script
USE_REMOTE=false

if [ "$USE_REMOTE" = true ]; then
	blastp -query "$INPUT" -remote -num_threads "$THREADS" -evalue "$EVALUE" -max_target_seqs "$MAX_TARGETS" -outfmt "6 qseqid sseqid pident length evalue bitscore stitle" >> "$OUTPUT"
else
	blastp -query "$INPUT" -db "$DB" -num_threads "$THREADS" -evalue "$EVALUE" -max_target_seqs "$MAX_TARGETS" -outfmt "6 qseqid sseqid pident length evalue bitscore stitle" >> "$OUTPUT"
fi
```

Con `-remote` la búsqueda se realiza contra el servidor BLAST de NCBI/EBI y no necesita base local, pero depende de la conectividad y de límites de uso.

Script de BLAST local (nota importante)
-------------------------------------

El script `pipeline-blast_local/blast_analizar_top3hits.sh` actualmente valida la existencia de la base de datos con `blastdbcmd -db "$DB" -info`. Si decide usar una DB local, asegúrese de que la ruta y el prefijo coincidan con lo creado por `makeblastdb`. Si elige `-remote`, quite o adapte esa validación.

Recomendaciones de recursos
---------------------------

- Swiss‑Prot es relativamente grande (centenas de MB/GB comprimido). Asegúrese de tener suficiente espacio en disco y tiempo para descargar y construir la DB (CPU y RAM para `makeblastdb`).
- Para análisis en servidores o despliegues, prefiera construir la DB en un disco rápido y compartirla entre trabajos.

Descripción detallada de archivos
---------------------------------

- `diseno-primers/main.py`: Interfaz CLI. Valida entradas, crea directorio de salida, registra estadísticas y orquesta llamadas a `PrimerDesigner` y `RestrictionAnalyzer`.
- `diseno-primers/primer_pipeline/designer.py`: Implementa `PrimerDesigner` (carga secuencias, parseo GFF, diseño de primers, guardado de resultados).
- `diseno-primers/primer_pipeline/analyzer.py`: Implementa `RestrictionAnalyzer` (búsqueda de sitios de restricción usando un diccionario simple de enzimas).
- `diseno-primers/primer_pipeline/utils.py`: Funciones utilitarias (complemento reverso, conversión IUPAC → regex).
- `pipeline-blast_local/blast_analizar_top3hits.sh`: Script con formato y barra de progreso para ejecutar BLASTp contra una DB local Swiss‑Prot.

Ejecución de ejemplo completa
-----------------------------

# 1) Diseñar primers y analizar amplicones
```bash
cd diseno-primers
python3 main.py -f example_data/genoma.fasta -g example_data/genes.gff -o ../resultado
```

# 2) (Opcional) Ejecutar BLASTp local contra Swiss‑Prot
```bash
cd pipeline-blast_local
# ajustar INPUT, DB y THREADS dentro del script o exportar variables antes
./blast_analizar_top3hits.sh
```

Solución de problemas comunes
----------------------------

- "ERROR: Se requiere biopython": instale dependencias con `pip install -r diseno-primers/requirements.txt`.
- "blastp no está instalado": instale BLAST+ como se indica arriba.
- "La base de datos local Swiss-Prot no pudo ser inicializada": verifique que la ruta `DB` apunte al prefijo correcto creado por `makeblastdb`.

Contribuciones y contacto
-------------------------

Este repositorio fue desarrollado por Barbara Sara, Emilia Vergara y Matías Ríos como parte de la materia *Bioinformática 2* (FI-UNER). Para dudas o sugerencias escriba a: bioinfortics.g3@ingenieria.uner.edu.ar

Licencia
--------

Distribuido sin licencia explícita. Para uso académico cite a los autores y la asignatura.

¿Qué sigue?
-----------

- ¿Quiere que actualice `pipeline-blast_local/blast_analizar_top3hits.sh` para soportar `-remote` vía flag (opcional)?
- ¿Desea que incorpore un instalador (Makefile / script) para descargar y construir Swiss‑Prot automáticamente?

---

Archivo actualizado por el equipo — documentación ampliada y pasos operativos claros.
