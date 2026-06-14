# primer_pipeline/designer.py
"""
Módulo encargado de la lectura de archivos biológicos y diseño de primers.
"""

import sys
from .utils import reverse_complement

try:
    from Bio import SeqIO
except ImportError:
    print("ERROR: Se requiere biopython. Instálalo con: pip install biopython")
    sys.exit(1)


class PrimerDesigner:
    """Diseñador de primers con cálculo de Tm."""
    
    def __init__(self, fasta_file: str, gff_file: str):
        self.fasta_file = fasta_file
        self.gff_file = gff_file
        self.sequence = None
        self.sequence_id = None
        self.genes = []
        self.primers = {}
        self.products = {}
        
    def load_sequence(self) -> bool:
        """Carga la secuencia del archivo FASTA."""
        try:
            print("[*] Cargando secuencia FASTA...")
            fasta_seqs = list(SeqIO.parse(self.fasta_file, "fasta"))
            if not fasta_seqs:
                print("ERROR: No se encontraron secuencias en el archivo FASTA")
                return False
            
            record = fasta_seqs[0]
            self.sequence = str(record.seq).upper()
            self.sequence_id = record.id
            print(f"    ✓ Secuencia cargada: {len(self.sequence)} bp")
            return True
        except Exception as e:
            print(f"ERROR al cargar FASTA: {e}")
            return False
    
    def load_gff(self) -> bool:
        """Carga genes del archivo GFF."""
        try:
            print("[*] Cargando anotaciones GFF...")
            with open(self.gff_file, 'r') as f:
                for line in f:
                    if line.startswith('#'):
                        continue
                    fields = line.strip().split('\t')
                    if len(fields) < 9:
                        continue
                    
                    seqid, source, feature, start, end, score, strand, frame, attrs = fields
                    
                    if feature != 'CDS':
                        continue
                    
                    gene_name = None
                    for attr in attrs.split(';'):
                        if attr.startswith('ID='):
                            gene_name = attr.split('=')[1]
                            break
                    
                    if not gene_name:
                        gene_name = f"gene_{len(self.genes)+1}"
                    
                    self.genes.append({
                        'name': gene_name,
                        'start': int(start) - 1,
                        'end': int(end),
                        'strand': strand,
                        'length': int(end) - int(start) + 1
                    })
            
            print(f"    ✓ {len(self.genes)} genes cargados")
            return True
        except Exception as e:
            print(f"ERROR al cargar GFF: {e}")
            return False
    
    def calculate_tm(self, primer_seq: str) -> float:
        """Calcula temperatura de melting usando fórmulas empíricas según longitud."""
        if len(primer_seq) < 14:
            return 4 * (primer_seq.count('G') + primer_seq.count('C')) + \
                   2 * (primer_seq.count('A') + primer_seq.count('T'))
        
        gc_count = primer_seq.count('G') + primer_seq.count('C')
        at_count = primer_seq.count('A') + primer_seq.count('T')
        tm = 64.9 + 41 * (gc_count - 16.4) / (at_count + gc_count)
        return round(tm, 2)
    
    def design_primers(self) -> bool:
        """Diseña primers para todos los genes cargados."""
        print("[*] Diseñando primers...")
        if not self.sequence or not self.genes:
            print("ERROR: Cargar secuencia y genes primero")
            return False
        
        for gene in self.genes:
            start = gene['start']
            end = gene['end']
            strand = gene['strand']
            name = gene['name']
            
            if end > len(self.sequence):
                print(f"    ⚠ Gen {name}: coordenada fuera de rango")
                continue
            
            gene_seq = self.sequence[start:end]
            if strand == '-':
                gene_seq = reverse_complement(gene_seq)
            
            fw_primer = gene_seq[:20]
            rv_primer_pos = gene_seq[-20:]
            rv_primer = reverse_complement(rv_primer_pos)
            
            tm_fw = self.calculate_tm(fw_primer)
            ta_fw = tm_fw - 5
            tm_rv = self.calculate_tm(rv_primer)
            ta_rv = tm_rv - 5
            
            self.primers[name] = {
                'fw_primer': fw_primer,
                'tm_fw': tm_fw,
                'ta_fw': ta_fw,
                'rv_primer': rv_primer,
                'tm_rv': tm_rv,
                'ta_rv': ta_rv,
                'product_size': len(gene_seq)
            }
            self.products[name] = gene_seq
        
        print(f"    ✓ {len(self.primers)} pares de primers diseñados")
        return True
    
    def save_primers_tab(self, output_file: str) -> bool:
        """Guarda primers en formato tabular."""
        try:
            print(f"[*] Guardando primers en {output_file}...")
            with open(output_file, 'w') as f:
                f.write("Gen\tPrimer_FW\tTm_FW\tTa_FW\tPrimer_RV\tTm_RV\tTa_RV\tTamaño_Producto\n")
                for gene_name in sorted(self.primers.keys()):
                    p = self.primers[gene_name]
                    f.write(f"{gene_name}\t{p['fw_primer']}\t{p['tm_fw']}\t"
                            f"{p['ta_fw']}\t{p['rv_primer']}\t{p['tm_rv']}\t"
                            f"{p['ta_rv']}\t{p['product_size']}\n")
            return True
        except Exception as e:
            print(f"ERROR al guardar primers: {e}")
            return False
    
    def save_products_fasta(self, output_file: str) -> bool:
        """Guarda productos de PCR en formato multiFASTA."""
        try:
            print(f"[*] Guardando productos de PCR en {output_file}...")
            with open(output_file, 'w') as f:
                for gene_name in sorted(self.products.keys()):
                    product_seq = self.products[gene_name]
                    f.write(f">Amplicon_{gene_name}_{len(product_seq)}\n")
                    for i in range(0, len(product_seq), 70):
                        f.write(product_seq[i:i+70] + '\n')
            return True
        except Exception as e:
            print(f"ERROR al guardar productos: {e}")
            return False