import numpy as np
from wavelet_1d import wavelet1d_direct, wavelet1d_inverse

def wavelet2d_direct(image, h, g, levels=1):
    """
    Transformée en ondelettes 2D (analyse)
    image : ndarray 2D
    h, g : filtres d’analyse 1D
    levels : nombre de niveaux
    """
    img = image.copy()
    rows, cols = img.shape

    for level in range(levels):
        r, c = rows // (2**level), cols // (2**level)

        # Appliquer 1D sur les lignes
        for i in range(r):
            approx, detail = wavelet1d_direct(img[i, :c], h, g)
            img[i, :c//2] = approx
            img[i, c//2:c] = detail

        # Appliquer 1D sur les colonnes
        for j in range(c):
            col = img[:r, j]
            approx, detail = wavelet1d_direct(col, h, g)
            img[:r//2, j] = approx
            img[r//2:r, j] = detail

    return img


def wavelet2d_inverse(coeffs, hr, gr, levels=1):
    """
    Transformée inverse 2D (synthèse)
    coeffs : ndarray 2D (coefficients)
    hr, gr : filtres de reconstruction 1D
    levels : nombre de niveaux
    """
    img = coeffs.copy()
    rows, cols = img.shape

    for level in reversed(range(levels)):
        r, c = rows // (2**level), cols // (2**level)

        # Colonnes inverse
        for j in range(c):
            approx = img[:r//2, j]
            detail = img[r//2:r, j]
            img[:r, j] = wavelet1d_inverse(approx, detail, hr, gr)

        # Lignes inverse
        for i in range(r):
            approx = img[i, :c//2]
            detail = img[i, c//2:c]
            img[i, :c] = wavelet1d_inverse(approx, detail, hr, gr)

    return img
