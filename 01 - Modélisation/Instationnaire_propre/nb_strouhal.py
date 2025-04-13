import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# 1. Définir le répertoire courant comme celui où se trouve le script
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# 2. Nom du fichier CSV
# Exemple : "Max_V_sur_X_Re200_D1.csv" ou "Max_V_sur_X_Re500_D1.5.csv"
filename = "Max_V_sur_Y_Re200_D1.csv"  # à modifier selon le cas

# 3. Extraction des paramètres Re et D depuis le nom de fichier
# Le pattern recherche "_Re" suivi d'un ou plusieurs chiffres, puis "_D" suivi d'un ou plusieurs chiffres éventuellement avec un point.
pattern = r"_Re(\d+)_D([\d\.]+)\.csv"
match = re.search(pattern, filename)
if match:
    Re_val = float(match.group(1))
    D_val = float(match.group(2))
    print(f"Re extrait : {Re_val}")
    print(f"D extrait : {D_val} m")
else:
    raise ValueError("Le nom du fichier ne contient pas les informations Re et D au format attendu.")

# 4. Calcul de U0
# Pour l'air, on suppose la viscosité cinématique (nu) égale à 1.47e-5 m²/s.
nu = 1.47e-5  
U0 = Re_val * nu / D_val
print(f"Vitesse libre U0 calculée : {U0:.4f} m/s")

# 5. Lecture du fichier CSV
df = pd.read_csv(filename)
col_time = "Time"
col_vel  = "Max_vitesse_au_point_y Monitor: Max_vitesse_au_point_y Monitor (m/s)"
time = df[col_time].values
velocity = df[col_vel].values

# 6. Plot du signal complet pour visualisation
plt.figure(figsize=(8,5))
plt.plot(time, velocity, label="Vitesse max point y")
plt.xlabel("Temps (s)")
plt.ylabel("Vitesse (m/s)")
plt.title("Évolution de la vitesse au point y")
plt.grid(True)
plt.legend()
plt.savefig("vitesse_au_point_y.png", dpi=300)
plt.show()

# 7. Détection des pics dans le signal
# On utilise find_peaks, ajustez 'prominence' si besoin.
peaks, properties = find_peaks(velocity, prominence=1e-12)
peak_times = time[peaks]

if len(peak_times) < 4:
    print("Nombre de pics insuffisant pour déterminer la périodicité de la partie finale.")
else:
    # Utiliser uniquement les 4 derniers pics (donc 3 intervalles) pour être sûr que le phénomène est bien périodique
    last_peak_times = peak_times[-4:]
    dt_peaks = np.diff(last_peak_times)
    period = np.mean(dt_peaks)
    frequency = 1.0 / period

    print(f"Nombre total de pics détectés : {len(peaks)}")
    print(f"Période moyenne (sur les 3 derniers intervalles) : {period:.4f} s")
    print(f"Fréquence moyenne : {frequency:.4f} Hz")

    # 8. Calcul du nombre de Strouhal
    # Formule : St = (f * D) / U0
    St = frequency * D_val / U0
    print(f"Nombre de Strouhal (St) : {St:.4f}")

    # Tracé du signal avec les pics détectés (affichage complet et sur la partie finale)
    plt.figure(figsize=(8,5))
    plt.plot(time, velocity, label="Vitesse max point y")
    plt.plot(peak_times, velocity[peaks], "rx", label="Pics détectés")
    plt.xlabel("Temps (s)")
    plt.ylabel("Vitesse (m/s)")
    plt.title("Détection de pics pour le calcul de la période et de Strouhal")
    plt.grid(True)
    plt.legend()
    plt.savefig("vitesse_au_point_y_peaks.png", dpi=300)
    plt.show()
