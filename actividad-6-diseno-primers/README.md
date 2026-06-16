# Pipeline de diseño de primers para Brucella suis

Este proyecto contiene un pipeline en Python para diseñar primers de PCR específicos a partir de una secuencia genómica en formato FASTA y anotaciones de genes en formato GFF.

## Requisitos

- Python 3
- Biopython

Instala Biopython con:

```bash
pip install biopython
```

## Archivos principales

- `diseñar_primers.py`: script principal para ejecutar el pipeline.
- `primer_pipeline/designer.py`: carga FASTA/GFF y diseña los primers.
- `primer_pipeline/analyzer.py`: analiza sitios de restricción en los amplicones.
- `primer_pipeline/utils.py`: utilidades de secuencias de ADN.

## Uso

Desde la carpeta del proyecto, ejecuta:

```bash
cd /home/matias/Escritorio/TIF-Bioinfo2-G3/actividad-6-diseno-primers
python3 diseñar_primers.py -f <archivo_fasta> -g <archivo_gff> -o <directorio_salida>
```

### Ejemplo

Si tienes los archivos en `data/`, usa:

```bash
python3 diseñar_primers.py -f data/scaffolds.fasta -g data/brucella_hybrid.gff -o resultados
```

## Parámetros

- `-f`, `--fasta`: archivo FASTA con la secuencia genómica.
- `-g`, `--gff`: archivo GFF con las anotaciones de genes.
- `-o`, `--output`: directorio de salida. Si no se especifica, usa el directorio actual.

## Archivos de salida

El script genera los siguientes archivos dentro del directorio de salida:

- `res_primers.tab`
- `res_prod.fa`
- `res_enzimas.tab`
- `pipeline.stdout.log`
- `pipeline.stderr.log`

## Notas

- El script valida que existan los archivos FASTA y GFF antes de correr.
- Si el directorio de salida no existe, lo crea automáticamente.
