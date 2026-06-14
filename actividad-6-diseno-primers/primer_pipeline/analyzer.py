# primer_pipeline/analyzer.py
"""
Módulo para el análisis enzimático de restricción en productos de PCR amplificados.
"""

import re
from typing import Dict
from .utils import iupac_to_regex


class RestrictionAnalyzer:
    """Analizador de sitios de restricción en secuencias nucleotídicas."""
    
    RESTRICTION_ENZYMES = {
        'EcoRI': 'GAATTC',
        'BamHI': 'GGATCC',
        'AvaII': 'GGWCC'
    }
    
    def __init__(self, products_dict: Dict[str, str]):
        self.products = products_dict
        self.results = []
    
    def find_restriction_sites(self) -> bool:
        """Busca sitios de restricción en todos los productos guardados."""
        print("[*] Analizando sitios de restricción...")
        
        for gene_name, product_seq in self.products.items():
            for enzyme_name, site_pattern in self.RESTRICTION_ENZYMES.items():
                regex_pattern = iupac_to_regex(site_pattern)
                matches = list(re.finditer(regex_pattern, product_seq, re.IGNORECASE))
                
                self.results.append({
                    'amplicon': gene_name,
                    'enzyme': enzyme_name,
                    'site': site_pattern,
                    'count': len(matches)
                })
        
        print(f"    ✓ Análisis completado para {len(self.products)} amplicones")
        return True
    
    def save_results(self, output_file: str) -> bool:
        """Guarda los resultados del análisis en un archivo TSV."""
        try:
            print(f"[*] Guardando análisis de restricción en {output_file}...")
            with open(output_file, 'w') as f:
                f.write("Amplicón\tEnzima\tSitio\tCantidad\n")
                for result in sorted(self.results, key=lambda x: (x['amplicon'], x['enzyme'])):
                    f.write(f"{result['amplicon']}\t{result['enzyme']}\t"
                            f"{result['site']}\t{result['count']}\n")
            return True
        except Exception as e:
            print(f"ERROR al guardar restricción: {e}")
            return False