"""
Módulo encargado de la lectura de archivos biológicos, diseño de primers
y análisis de sitios de restricción para el kit diagnóstico de Brucella suis.
"""

import sys
from primer_pipeline.utils import reverse_complement
from primer_pipeline.analyzer import RestrictionAnalyzer
from primer_pipeline.designer import PrimerDesigner

try:
    from Bio import SeqIO
except ImportError:
    print("ERROR: Se requiere biopython. Instálalo con: pip install biopython")
    sys.exit(1)



if __name__ == "__main__":
    # CONTROL DE ENTRADAS POR CONSOLA (Cumple requisito estricto de la consigna)
    if len(sys.argv) < 3:
        print("\nERROR: Faltan archivos de entrada.")
        print("Uso correcto: python diseñar_primers.py <archivo_fasta> <archivo_gff>")
        print("Ejemplo: python diseñar_primers.py data/scaffolds.fasta data/brucella_hybrid.gff\n")
        sys.exit(1)
        
    archivo_fasta = sys.argv[1]
    archivo_gff = sys.argv[2]
    
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