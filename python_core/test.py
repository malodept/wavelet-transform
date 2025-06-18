import numpy as np
from math import sqrt
from wavelet_1d import wavelet1d_direct, wavelet1d_inverse

# Signal d'exemple
signal = np.array([4, 6, 10, 12, 14, 8, 6, 2], dtype=float)

# Filtres Haar
h = np.array([1/sqrt(2), 1/sqrt(2)])
g = np.array([1/sqrt(2), -1/sqrt(2)])

# Transformée directe
approx, detail = wavelet1d_direct(signal, h, g)

# Reconstruction
reconstr = wavelet1d_inverse(approx, detail, h, g)

# Affichage
print("Signal original   :", signal)
print("Approximation     :", approx)
print("Détail            :", detail)
print("Signal reconstruit:", reconstr)


################################################################



from wavelet_2d import wavelet2d_direct, wavelet2d_inverse

# Créer une matrice simple
matrix = np.array([
    [4, 6, 10, 12],
    [14, 8, 6, 2],
    [1, 3, 7, 9],
    [13, 11, 5, 0]
], dtype=float)

h = np.array([1/np.sqrt(2), 1/np.sqrt(2)])
g = np.array([1/np.sqrt(2), -1/np.sqrt(2)])

# Analyse
coeffs = wavelet2d_direct(matrix, h, g, levels=1)
print("Coefficients 2D :\n", np.round(coeffs, 2))

# Synthèse
reconstructed = wavelet2d_inverse(coeffs, h, g, levels=1)
print("Reconstruit :\n", np.round(reconstructed, 2))

import matplotlib.pyplot as plt




from quantization import quantify, entropy

delta = 5
quantized_coeffs = quantify(coeffs, delta)
print(f"Coefficients quantifiés (delta = {delta}):\n", quantized_coeffs)

H = entropy(quantized_coeffs)
print(f"Entropie des coefficients quantifiés : {H:.4f} bits")
