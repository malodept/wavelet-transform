import sys
import numpy as np
from PIL import Image
from wavelet_2d import wavelet2d_direct, wavelet2d_inverse
from quantization import quantify, entropy
from math import sqrt
import os


# --- Lecture des arguments ---
if len(sys.argv) < 3:
    print("Usage: python process_image.py <levels> <delta>")
    sys.exit(1)

levels = int(sys.argv[1])
delta = float(sys.argv[2])

# --- Chargement de l’image ---
img_path = "../shared/input.png"
image = Image.open(img_path).convert("L")
img_array = np.array(image).astype(float)

# --- Filtres Haar ---
h = np.array([1/sqrt(2), 1/sqrt(2)])
g = np.array([1/sqrt(2), -1/sqrt(2)])

# --- Analyse ondelettes ---
coeffs = wavelet2d_direct(img_array, h, g, levels=levels)

# --- Quantification ---
q_coeffs = quantify(coeffs, delta)

# Lire les coordonnées si elles existent
if os.path.exists("shared/zerosub.txt"):
    with open("shared/zerosub.txt", "r") as f:
        x1, y1, x2, y2 = map(int, f.read().split())

    # Conversion aux coordonnées de l’image
    xmin, xmax = min(x1, x2), max(x1, x2)
    ymin, ymax = min(y1, y2), max(y1, y2)

    # On met à zéro les coefficients dans cette zone
    q_coeffs[ymin:ymax, xmin:xmax] = 0


# --- Entropie ---
H = entropy(q_coeffs)
with open("../shared/entropy.txt", "w") as f:
    f.write(f"{H:.4f} bits")

# --- Reconstruction ---
reconstructed = wavelet2d_inverse(q_coeffs, h, g, levels=levels)
reconstructed = np.clip(reconstructed, 0, 255).astype(np.uint8)

# --- Sauvegarde résultats ---
np.save("../shared/transform.npy", q_coeffs)
Image.fromarray(reconstructed).save("../shared/output.png")
