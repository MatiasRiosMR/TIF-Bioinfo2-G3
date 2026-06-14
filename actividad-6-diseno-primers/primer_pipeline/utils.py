# primer_pipeline/utils.py
"""
Funciones utilitarias para procesamiento de secuencias de ADN.
"""

def reverse_complement(seq: str) -> str:
    """Genera el complemento reverso de una secuencia de nucleótidos (incluye IUPAC)."""
    complement = {
        'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G',
        'N': 'N', 'W': 'W', 'S': 'S', 'K': 'K',
        'M': 'M', 'R': 'R', 'Y': 'Y', 'B': 'B',
        'D': 'D', 'H': 'H', 'V': 'V'
    }
    return ''.join(complement.get(base, 'N') for base in reversed(seq))


def iupac_to_regex(pattern: str) -> str:
    """Convierte un patrón de secuencia IUPAC a una expresión regular compatible con re."""
    iupac_map = {
        'W': '[AT]', 'S': '[GC]', 'K': '[GT]', 'M': '[AC]',
        'R': '[AG]', 'Y': '[CT]', 'B': '[CGT]', 'D': '[AGT]',
        'H': '[ACT]', 'V': '[ACG]', 'N': '[ACGT]'
    }
    regex = pattern
    for iupac, bases in iupac_map.items():
        regex = regex.replace(iupac, bases)
    return regex