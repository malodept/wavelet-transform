import sys
import numpy as np
from PIL import Image
from wavelet_2d import wavelet2d_direct, wavelet2d_inverse
from quantization import quantify, entropy
from math import sqrt
import os
import matplotlib.pyplot as plt

# Lecture des arguments
if len(sys.argv) < 3:
    print("Usage: python process_image.py <levels> <delta>")
    sys.exit(1)

levels = int(sys.argv[1])
delta = float(sys.argv[2])

# Chargement de l’image
img_path = "shared/input.png"
image = Image.open(img_path).convert("L")
img_array = np.array(image).astype(float)

# Filtres Haar
h = np.array([1/sqrt(2), 1/sqrt(2)])
g = np.array([1/sqrt(2), -1/sqrt(2)])

# Analyse + quantification
coeffs = wavelet2d_direct(img_array, h, g, levels=levels)
q_coeffs_base = quantify(coeffs.copy(), delta)
q_coeffs_masked = q_coeffs_base.copy()

# Mise à zéro si rectangle défini
if os.path.exists("shared/zerosub.txt"):
    with open("shared/zerosub.txt", "r") as f:
        x1, y1, x2, y2 = map(int, f.read().split())
    xmin, xmax = min(x1, x2), max(x1, x2)
    ymin, ymax = min(y1, y2), max(y1, y2)
    q_coeffs_masked[ymin:ymax, xmin:xmax] = 0

# Reconstruction sans suppression
output_base = wavelet2d_inverse(q_coeffs_base, h, g, levels=levels)
output_base = np.clip(output_base, 0, 255).astype(np.uint8)
Image.fromarray(output_base).save("shared/output_base.png")

# Reconstruction avec suppression
output_masked = wavelet2d_inverse(q_coeffs_masked, h, g, levels=levels)
output_masked = np.clip(output_masked, 0, 255).astype(np.uint8)
Image.fromarray(output_masked).save("shared/output.png")

# Différence entre les deux
diff_mask = np.abs(output_base.astype(float) - output_masked.astype(float))
diff_mask = np.clip(diff_mask, 0, 255).astype(np.uint8)
Image.fromarray(diff_mask).save("shared/diff_mask.png")

# Entropie
H = entropy(q_coeffs_masked)
with open("shared/entropy.txt", "w") as f:
    f.write(f"{H:.4f} bits")

# Sauvegarde des coefficients
np.save("shared/transform.npy", q_coeffs_masked)

# Affichage coefficients
plt.figure(figsize=(6, 6))
plt.imshow(np.abs(q_coeffs_masked), cmap='gray', vmin=0, vmax=np.max(np.abs(q_coeffs_masked)))
plt.title("Coefficients après quantification et mise à zéro")
plt.axis('off')
plt.tight_layout()
plt.savefig("shared/coeffs.png")
plt.close()

# Mesures quantitatives
mse = np.mean((output_base - output_masked) ** 2)
psnr = float('inf') if mse == 0 else 20 * np.log10(255.0 / np.sqrt(mse))

with open("shared/metrics.txt", "w") as f:
    f.write(f"MSE: {mse:.4f}\n")
    f.write(f"PSNR: {psnr:.2f} dB\n")
    f.write(f"Entropie: {H:.4f} bits\n")
