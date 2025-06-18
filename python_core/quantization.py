import numpy as np
from collections import Counter
from math import log2

def quantify(coeffs, delta):
    """
    Quantification uniforme des coefficients (arrondi)
    Sauf le coefficient DC [0,0] qui est laissé inchangé
    """
    quantized = coeffs.copy()
    for i in range(coeffs.shape[0]):
        for j in range(coeffs.shape[1]):
            if i == 0 and j == 0:
                continue  # ne pas quantifier le coefficient DC
            quantized[i, j] = round(coeffs[i, j] / delta) * delta
    return quantized


def entropy(coeffs):
    """
    Calcule l'entropie de Shannon (en bits) des coefficients
    """
    flat = coeffs.flatten()
    
    # Convertir en entiers pour calculer une distribution propre
    values = flat.astype(int)
    freq = Counter(values)
    total = len(values)
    
    ent = 0.0
    for count in freq.values():
        p = count / total
        ent -= p * log2(p)
    return ent
