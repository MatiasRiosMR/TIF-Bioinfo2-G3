#!/usr/bin/env bash

set -euo pipefail

############################
# CONFIGURACIÓN
############################

INPUT="brucella_hybrid.faa"
OUTPUT="blast_swissprot.tsv"
LOG="blast_swissprot.log"
DB="./db/swissprot"

EVALUE="1e-5"
MAX_TARGETS=3
THREADS=8

# Paleta de Colores ANSI (Bold e Institucionales)
B_BLUE='\033[1;34m'
B_CYAN='\033[1;36m'
B_GREEN='\033[1;32m'
B_YELLOW='\033[1;33m'
B_RED='\033[1;31m'
B_WHITE='\033[1;37m'
DIM='\033[2m'
NC='\033[0m' # Reset

############################
# FUNCIONES DE LOG Y SALIDA
############################

: > "$LOG"

log_info() {
    local datetime
    datetime=$(date '+%H:%M:%S')
    echo -e "${B_GREEN}[INFO]${NC} [${DIM}${datetime}${NC}] ${B_WHITE}$1${NC}"
    echo "[INFO] [$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG"
}

log_status() {
    local datetime
    datetime=$(date '+%H:%M:%S')
    echo -e "${B_CYAN}[STATUS]${NC} [${DIM}${datetime}${NC}] $1"
    echo "[STATUS] [$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG"
}

log_error() {
    local datetime
    datetime=$(date '+%H:%M:%S')
    echo -e "${B_RED}[ERROR] [${datetime}] $1${NC}" >&2
    echo "[ERROR] [$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG"
}

log_raw() {
    echo -e "$1"
    echo "$1" | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[mGK]//g" >> "$LOG"
}

############################
# INTERFAZ INSTITUCIONAL
############################

clear
log_raw "${B_BLUE}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓${NC}"
log_raw "${B_BLUE}┃${NC}            ${B_WHITE}UNIVERSIDAD NACIONAL DE ENTRE RÍOS (UNER)${NC}            ${B_BLUE}┃${NC}"
log_raw "${B_BLUE}┃${NC}                      ${B_CYAN}FACULTAD DE INGENIERÍA${NC}                      ${B_BLUE}┃${NC}"
log_raw "${B_BLUE}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛${NC}"
log_raw " Carrera:  Licenciatura en Bioinformática"
log_raw " Materia:  Bioinformática 2 / Análisis y Alineamientos de Secuencias"
log_raw " Trabajo:  Trabajo Integrador Final"
log_raw " Alumnos:  ${B_WHITE}Barbara Sara, Vergara Emilia, Rios Matias${NC}"
log_raw "${B_BLUE}────────────────────────────────────────────────────────────────────${NC}"
log_raw "                    ${B_YELLOW}PARÁMETROS DE CONFIGURACIÓN${NC}                  "
log_raw "${B_BLUE}────────────────────────────────────────────────────────────────────${NC}"
log_raw "  • Archivo Input:   ${B_WHITE}$INPUT${NC}"
log_raw "  • Base de Datos:   ${DIM}$DB${NC}"
log_raw "  • Umbral E-value:  ${B_GREEN}$EVALUE${NC}"
log_raw "  • Máximos Hits:    ${B_GREEN}$MAX_TARGETS por query${NC}"
log_raw "  • Hilos (CPUs):    ${B_GREEN}$THREADS cores${NC}"
log_raw "  • Archivo Output:  ${B_YELLOW}$OUTPUT${NC}"
log_raw "  • Archivo Log:     ${B_YELLOW}$LOG${NC}"
log_raw "${B_BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

############################
# VALIDACIONES (CHECKS)
############################

log_status "Validando requerimientos del sistema y consistencia de archivos..."

if [[ ! -f "$INPUT" ]]; then
    log_error "No se encontró el archivo FASTA de entrada: '$INPUT'"
    exit 1
fi

if ! command -v blastp >/dev/null 2>&1; then
    log_error "El ejecutable 'blastp' no está instalado o no se encuentra en el PATH."
    exit 1
fi

if ! blastdbcmd -db "$DB" -info >/dev/null 2>&1; then
    log_error "La base de datos local Swiss-Prot no pudo ser inicializada en: '$DB'"
    exit 1
fi

log_info "Entorno y dependencias verificadas correctamente."

############################
# PROCESAMIENTO PREVIO
############################

TOTAL=$(grep -c "^>" "$INPUT")
log_info "Total de secuencias identificadas en el input: ${B_CYAN}$TOTAL${NC}"

# Inicializar archivo de salida con su correspondiente cabecera
echo -e "qseqid\tsseqid\tpident\tlength\tqcovs\tevalue\tbitscore\ttitle" > "$OUTPUT"

############################
# EJECUCIÓN DEL ALINEAMIENTO LOCAL
############################

log_status "Iniciando la ejecución del algoritmo BLASTp..."
echo ""

# Caracteres del indicador de actividad en paralelo
SPINNER="⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
SPIN_IDX=0

# Ejecución de BLASTp en segundo plano
blastp \
  -query "$INPUT" \
  -db "$DB" \
  -num_threads "$THREADS" \
  -evalue "$EVALUE" \
  -max_target_seqs "$MAX_TARGETS" \
  -outfmt "6 qseqid sseqid pident length qcovs evalue bitscore stitle" >> "$OUTPUT" 2>> "$LOG" &

BLAST_PID=$!

# Monitoreo interactivo del proceso de cómputo
while kill -0 "$BLAST_PID" 2>/dev/null; do
    if [[ -f "$OUTPUT" ]]; then
        LINEAS=$(wc -l < "$OUTPUT")
        CURRENT=$(( LINEAS - 1 ))
        [[ $CURRENT -lt 0 ]] && CURRENT=0
    else
        CURRENT=0
    fi
    
    # Estimación del porcentaje de avance
    MAX_ESTIMATED=$(( TOTAL * MAX_TARGETS ))
    if [[ $MAX_ESTIMATED -gt 0 ]]; then
        PERCENT=$(( CURRENT * 100 / MAX_ESTIMATED ))
        [[ $PERCENT -gt 97 ]] && PERCENT=97 
    else
        PERCENT=0
    fi
    
    # Construcción de la matriz gráfica de la barra de progreso
    BAR_WIDTH=40
    FILLED=$(( PERCENT * BAR_WIDTH / 100 ))
    EMPTY=$(( BAR_WIDTH - FILLED ))
    
    BAR_DONE=$(printf "%${FILLED}s" "" | tr ' ' '█')
    BAR_REMAINING=$(printf "%${EMPTY}s" "" | tr ' ' '░')
    
    CHAR="${SPINNER:$SPIN_IDX:1}"
    SPIN_IDX=$(( (SPIN_IDX + 1) % 10 ))
    
    # Salida por consola formateada sin saltos de línea
    printf "\r  ${B_YELLOW}%s${NC} Ejecutando alineamientos: [${B_GREEN}%s${DIM}%s${NC}] ${B_WHITE}%d%%${NC}" "$CHAR" "$BAR_DONE" "$BAR_REMAINING" "$PERCENT"
    
    sleep 0.15
done

# Sincronización del proceso de fondo
wait "$BLAST_PID"

# Actualización final de la barra al 100% ante la finalización exitosa
BAR_FULL=$(printf "%40s" "" | tr ' ' '█')
printf "\r  [OK] Ejecución completada:     [${B_GREEN}%s${NC}] ${B_GREEN}100%%${NC}\n" "$BAR_FULL"
echo ""

log_info "El análisis por homología de secuencias ha finalizado."

############################
# POST-PROCESAMIENTO: LIMPIEZA DE LA FUNCIÓN (TITLE)
############################

log_status "Filtrando descripciones de Swiss-Prot para extraer solo la función..."

TEMP_OUTPUT="${OUTPUT}.tmp"

awk -F'\t' '
BEGIN {OFS="\t"}
NR==1 {print; next} # Mantiene la cabecera intacta
{
    # Busca "RecName: Full=" y extrae el nombre limpio hasta el primer ";"
    if (match($8, /RecName: Full=[^;]+/)) {
        match_str = substr($8, RSTART, RLENGTH);
        sub(/RecName: Full=/, "", match_str);
        $8 = match_str;
    } 
    # Alternativa por si contiene la etiqueta "SubName"
    else if (match($8, /SubName: Full=[^;]+/)) {
        match_str = substr($8, RSTART, RLENGTH);
        sub(/SubName: Full=/, "", match_str);
        $8 = match_str;
    }
    print;
}' "$OUTPUT" > "$TEMP_OUTPUT"

# Reemplazar el archivo viejo por el nuevo limpio
mv "$TEMP_OUTPUT" "$OUTPUT"

############################
# FINALIZACIÓN Y REPORTE DE RUTAS
############################

echo ""
log_raw "${B_BLUE}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓${NC}"
log_raw "${B_BLUE}┃${NC}                 ${B_GREEN}PROCESO FINALIZADO CORRECTAMENTE${NC}                 ${B_BLUE}┃${NC}"
log_raw "${B_BLUE}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛${NC}"
log_raw " Los datos resultantes del análisis han sido estructurados y exportados:"
log_raw ""
log_raw "  • Matriz de Resultados (TSV):  ${B_WHITE}$(pwd)/$OUTPUT${NC}"
log_raw "  • Registro de Eventos (Log):   ${B_WHITE}$(pwd)/$LOG${NC}"
log_raw ""
log_raw " ──────────────────────────────────────────────────────────────────"
log_raw "  Agradecemos la utilización de este módulo de procesamiento local."
log_raw "  Desarrollado en el marco académico de la Facultad de Ingeniería."
log_raw "  Universidad Nacional de Entre Ríos."
log_raw "${B_BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
