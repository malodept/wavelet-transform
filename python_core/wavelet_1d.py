import numpy as np

def wavelet1d_direct(signal, h, g):
    """
    Transformée en ondelettes 1D directe (analyse)

    Args:
        signal (np.ndarray): Signal 1D (longueur paire)
        h (np.ndarray): Filtre passe-bas
        g (np.ndarray): Filtre passe-haut

    Returns:
        approx (np.ndarray): Coefficients d'approximation
        detail (np.ndarray): Coefficients de détail
    """
    N = len(signal)
    assert N % 2 == 0, "Le signal doit avoir une longueur paire"
    Nh = len(h)
    Ng = len(g)
    half = N // 2

    approx = np.zeros(half)
    detail = np.zeros(half)

    for i in range(half):
        for k in range(Nh):
            idx = 2 * i + k
            if idx < N:
                approx[i] += h[k] * signal[idx]
        for k in range(Ng):
            idx = 2 * i + k
            if idx < N:
                detail[i] += g[k] * signal[idx]

    return approx, detail


def wavelet1d_inverse(approx, detail, hr, gr):
    """
    Transformée en ondelettes 1D inverse (synthèse)

    Args:
        approx (np.ndarray): Coefficients d'approximation
        detail (np.ndarray): Coefficients de détail
        hr (np.ndarray): Filtre de reconstruction passe-bas
        gr (np.ndarray): Filtre de reconstruction passe-haut

    Returns:
        signal (np.ndarray): Signal reconstruit
    """
    half = len(approx)
    N = 2 * half
    Nhr = len(hr)
    Ngr = len(gr)

    signal = np.zeros(N)

    for i in range(half):
        for k in range(Nhr):
            idx = 2 * i + k
            if idx < N:
                signal[idx] += hr[k] * approx[i]
        for k in range(Ngr):
            idx = 2 * i + k
            if idx < N:
                signal[idx] += gr[k] * detail[i]

    return signal
