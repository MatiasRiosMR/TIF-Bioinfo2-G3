#!/usr/bin/env python3
# main.py
"""
Script ejecutable - Interfaz de Línea de Comandos (CLI)
Pipeline para diseño automático de primers específicos para Brucella suis.

Autor: Bioinformatics Team - Grupo 3
Institución: Facultad de Ingeniería - UNER

"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
import time


_stdout_log = None
_stderr_log = None


def write_stdout(message):
    print(message)
    if _stdout_log is not None:
        print(message, file=_stdout_log)


def write_stderr(message):
    print(message, file=sys.stderr)
    if _stderr_log is not None:
        print(message, file=_stderr_log)


# Importación de nuestros módulos empaquetados
from primer_pipeline import PrimerDesigner, RestrictionAnalyzer


def print_header():
    """Imprime el encabezado del programa."""
    write_stdout("\nPIPELINE DE DISEÑO DE PRIMERS PARA PCR")
    write_stdout("Brucella suis - Diagnóstico molecular")
    write_stdout("Versión: 1.0")
    write_stdout("Fuente: Facultad de Ingeniería - UNER\n")


def print_section(title):
    """Imprime el título de una sección."""
    write_stdout(f"\n{title}")
    write_stdout("" + "-" * len(title) + "\n")


def print_step(step_num, description):
    """Imprime el inicio de un paso."""
    write_stdout(f"Paso {step_num}: {description}")


def print_success(message, indent="    "):
    """Imprime un mensaje de éxito."""
    write_stdout(f"{indent}OK: {message}")


def print_info(message, indent="    "):
    """Imprime un mensaje informativo."""
    write_stdout(f"{indent}INFO: {message}")


def print_error(message, indent="    "):
    """Imprime un mensaje de error."""
    write_stderr(f"{indent}ERROR: {message}")


def print_footer(output_dir, primers_file, products_file, enzymes_file, stats):
    """Imprime el resumen final y estadísticas."""
    write_stdout("\nEJECUCIÓN COMPLETADA\n")
    print_section("RESUMEN")
    write_stdout("Archivos generados:")
    write_stdout(f"  {primers_file}")
    write_stdout(f"  {products_file}")
    write_stdout(f"  {enzymes_file}\n")
    write_stdout(f"Directorio de salida: {output_dir.absolute()}\n")
    write_stdout(f"Registro de salida: {output_dir / 'pipeline.stdout.log'}")
    write_stdout(f"Registro de errores: {output_dir / 'pipeline.stderr.log'}\n")
    write_stdout(f"Fecha de ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print_section("ESTADÍSTICAS")
    write_stdout(f"Genes procesados: {stats['genes_processed']}")
    write_stdout(f"Primers diseñados: {stats['primers_designed']}")
    write_stdout(f"Amplicones generados: {stats['amplicons_generated']}")
    write_stdout(f"Sitios de restricción encontrados: {stats['total_restriction_sites']}\n")

    if stats.get('enzyme_distribution'):
        write_stdout("Distribución de enzimas de restricción:")
        for enzyme, count in sorted(stats['enzyme_distribution'].items(), key=lambda x: x[1], reverse=True):
            write_stdout(f"  {enzyme:12} {count}")
        write_stdout("")

    if stats.get('amplicon_stats'):
        write_stdout("Estadísticas por amplicón:")
        write_stdout(f"  Mínimo de sitios: {stats['amplicon_stats']['min']}")
        write_stdout(f"  Máximo de sitios: {stats['amplicon_stats']['max']}")
        write_stdout(f"  Promedio de sitios: {stats['amplicon_stats']['avg']:.2f}\n")

    write_stdout(f"Tiempo de ejecución: {stats['execution_time']:.2f} segundos\n")
    write_stdout("Gracias por usar el pipeline.")
    write_stdout("Contacto: bioinfortics.g3@ingenieria.uner.edu.ar")


def validate_file(file_path, file_type):
    """Valida la existencia de un archivo y retorna el resultado."""
    if not Path(file_path).exists():
        print_error(f"No existe el archivo {file_type}: {file_path}")
        return False
    print_success(f"Archivo {file_type} encontrado: {file_path}")
    return True


def main():
    start_time = time.time()
    
    parser = argparse.ArgumentParser(
        description='Pipeline de diseño de primers para PCR - Brucella suis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EJEMPLOS DE USO:
    python3 main.py -f genoma.fasta -g genes.gff
    python3 main.py -f genoma.fasta -g genes.gff -o ./resultados
    python3 main.py --fasta genoma.fasta --gff genes.gff --output ./output

CONTACTO:
    Grupo Bioinformatics - G3: bioinfortics.g3@ingenieria.uner.edu.ar
        """
    )
    
    parser.add_argument(
        '-f', '--fasta', 
        required=True, 
        help='Archivo FASTA con la secuencia genómica'
    )
    parser.add_argument(
        '-g', '--gff', 
        required=True, 
        help='Archivo GFF con anotaciones de genes'
    )
    parser.add_argument(
        '-o', '--output', 
        default='.', 
        help='Directorio de salida (default: directorio actual)'
    )
    
    args = parser.parse_args()
    
    output_dir = Path(args.output)
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print_error(f"No se pudo crear el directorio de salida: {e}")
        sys.exit(1)

    stdout_log_path = output_dir / 'pipeline.stdout.log'
    stderr_log_path = output_dir / 'pipeline.stderr.log'
    with open(stdout_log_path, 'w') as stdout_log, open(stderr_log_path, 'w') as stderr_log:
        global _stdout_log, _stderr_log
        _stdout_log = stdout_log
        _stderr_log = stderr_log

        # Encabezado
        print_header()

        # Sección de validación
        print_section("VALIDACIÓN DE ARCHIVOS DE ENTRADA")

        if not validate_file(args.fasta, "FASTA"):
            sys.exit(1)

        if not validate_file(args.gff, "GFF"):
            sys.exit(1)

        print_success(f"Directorio de salida listo: {output_dir}")

        # Inicializar diccionario de estadísticas
        stats = {
            'genes_processed': 0,
            'primers_designed': 0,
            'amplicons_generated': 0,
            'total_restriction_sites': 0,
            'enzyme_distribution': {},
            'amplicon_stats': {'min': float('inf'), 'max': 0, 'total': 0, 'count': 0}
        }

        # Paso 1: Diseño de primers
        print_step(1, "DISEÑO DE PRIMERS PARA PCR")

        designer = PrimerDesigner(args.fasta, args.gff)

        if not designer.load_sequence():
            print_error("No se pudo cargar la secuencia FASTA", "     ")
            sys.exit(1)

        if not designer.load_gff():
            print_error("No se pudo cargar las anotaciones GFF", "     ")
            sys.exit(1)

        if not designer.design_primers():
            print_error("No se pudo diseñar los primers", "     ")
            sys.exit(1)

        # Recolectar estadísticas de Paso 1
        stats['genes_processed'] = len(designer.genes)
        stats['primers_designed'] = len(designer.primers)
        stats['amplicons_generated'] = len(designer.products)

        primers_output = output_dir / 'res_primers.tab'
        products_output = output_dir / 'res_prod.fa'

        if not designer.save_primers_tab(str(primers_output)):
            print_error("No se pudo guardar los primers", "     ")
            sys.exit(1)
        print_success(f"Tabla de primers generada: {primers_output.name}", "     ")

        if not designer.save_products_fasta(str(products_output)):
            print_error("No se pudo guardar los amplicones", "     ")
            sys.exit(1)
        print_success(f"Amplicones en FASTA generados: {products_output.name}", "     ")

        # Paso 2: Análisis de restricción
        print_step(2, "ANÁLISIS DE SITIOS DE RESTRICCIÓN")

        analyzer = RestrictionAnalyzer(designer.products)

        if not analyzer.find_restriction_sites():
            print_error("No se pudo analizar los sitios de restricción", "     ")
            sys.exit(1)

        enzymes_output = output_dir / 'res_enzimas.tab'

        if not analyzer.save_results(str(enzymes_output)):
            print_error("No se pudo guardar el análisis de restricción", "     ")
            sys.exit(1)
        print_success(f"Análisis de restricción generado: {enzymes_output.name}", "     ")

        # Recolectar estadísticas de Paso 2
        if analyzer.results:
            # Contar sitios totales y por enzima
            stats['total_restriction_sites'] = sum(r['count'] for r in analyzer.results)
            for result in analyzer.results:
                enzyme = result['enzyme']
                count = result['count']
                stats['enzyme_distribution'][enzyme] = stats['enzyme_distribution'].get(enzyme, 0) + count

            # Estadísticas por amplicón (mín, máx, promedio de sitios)
            amplicon_sites = {}
            for result in analyzer.results:
                amplicon = result['amplicon']
                count = result['count']
                amplicon_sites[amplicon] = amplicon_sites.get(amplicon, 0) + count

            if amplicon_sites:
                sites_values = list(amplicon_sites.values())
                stats['amplicon_stats']['min'] = min(sites_values)
                stats['amplicon_stats']['max'] = max(sites_values)
                stats['amplicon_stats']['avg'] = sum(sites_values) / len(sites_values)

        # Calcular tiempo de ejecución
        end_time = time.time()
        stats['execution_time'] = end_time - start_time

        # Pie de página con resumen final
        print_footer(output_dir, primers_output.name, products_output.name, enzymes_output.name, stats)


if __name__ == '__main__':
    main()