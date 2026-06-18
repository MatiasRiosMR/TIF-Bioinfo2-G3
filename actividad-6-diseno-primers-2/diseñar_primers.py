"""
Módulo encargado de la lectura de archivos biológicos, diseño de primers
y análisis de sitios de restricción para el kit diagnóstico de Brucella suis.
"""

import argparse
from primer_pipeline.utils import reverse_complement
from primer_pipeline.analyzer import RestrictionAnalyzer
from primer_pipeline.designer import PrimerDesigner



def parse_arguments():
    """Parsea los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Diseñador de primers para diagnóstico de Brucella suis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        
    )
    
    parser.add_argument(
        '-f', '--fasta',
        type=str,
        required=True,
        help='Archivo FASTA con la secuencia (obligatorio)'
    )
    
    parser.add_argument(
        '-g', '--gff',
        type=str,
        required=True,
        help='Archivo GFF con anotaciones de genes (obligatorio)'
    )
    
    return parser.parse_args()


if __name__ == "__main__":
    # Parsear argumentos con banderas
    args = parse_arguments()
    archivo_fasta = args.fasta
    archivo_gff = args.gff
    
    # Ejecución del Pipeline
    designer = PrimerDesigner(archivo_fasta, archivo_gff)
    
    if designer.load_sequence() and designer.load_gff():
        if designer.design_primers():
            # Guardado obligatorio
            designer.save_primers_tab("resultados/res_primers.tab")
            designer.save_products_fasta("resultados/res_prod.fa")
            
            # Análisis de restricción incorporado
            analyzer = RestrictionAnalyzer(designer.products)
            analyzer.find_restriction_sites()
            analyzer.save_results("resultados/res_enzimas.tab")
            
            print("\n[✓] ¡Pipeline completado con éxito! Todos los archivos requeridos se han generado.")
