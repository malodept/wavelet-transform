# 🌊 Wavelet Image Transform

Projet de traitement d’images par **transformée en ondelettes 2D** avec :

- Quantification des coefficients
- Suppression interactive de sous-bandes
- Visualisation des résultats
- Interface utilisateur en Java
- Traitement des images en Python




---

## 🚀 Fonctionnalités

L’interface permet :

- 📂 d’**ouvrir une image** (.png, convertie en niveaux de gris)
- 🔁 de **lancer la transformée en ondelettes** (analyse + reconstruction)
- 🔢 d’**entrer un pas de quantification** (`delta`) et un niveau de résolution (`niv_resol`)
- 🖱️ de **sélectionner une zone avec la souris** pour mettre à zéro ses coefficients
- 🔬 de **visualiser les résultats** :
  - image transformée (`output.png`)
  - coefficients (`coeffs.png`)
  - impact visuel (`diff_mask.png`)
  - mesures (`metrics.txt`)

---

## 🧠 Détail du traitement

1. **Transformée en ondelettes 2D** :
   - Basée sur la transformée de Haar
   - Séparable (ligne + colonne)
   - Plusieurs niveaux (`niv_resol`)

2. **Quantification uniforme** des coefficients :
   - Réduit l'information (compression)
   - Paramètre `delta`

3. **Mise à zéro** d’une zone rectangulaire :
   - Supprime les détails d’une sous-bande
   - Affecte visuellement la reconstruction

4. **Reconstruction de l’image**
   - Avec ou sans suppression

5. **Comparaison entre les deux reconstructions** :
   - Calcul de :
     - `diff_mask.png`
     - `MSE`, `PSNR`, `Entropie`

---

## 📊 Fichiers générés

| Fichier               | Description                                          |
|-----------------------|------------------------------------------------------|
| `output.png`          | Image reconstruite avec mise à zéro                 |
| `output_base.png`     | Image reconstruite sans suppression                 |
| `diff_mask.png`       | Différences entre les deux reconstructions          |
| `coeffs.png`          | Affichage des coefficients ondelettes (grisé)       |
| `metrics.txt`         | Mesures numériques (MSE, PSNR, Entropie)            |
| `transform.npy`       | Tableau numpy des coefficients quantifiés           |
| `entropy.txt`         | Entropie seule                                      |
| `zerosub.txt`         | Coordonnées de la zone sélectionnée (x1 y1 x2 y2)   |

---

## ▶️ Lancement

### 🎛 Interface Java

Depuis `wavelet_project/` :

```bash
javac java_ui/*.java
java java_ui.MainInterface

