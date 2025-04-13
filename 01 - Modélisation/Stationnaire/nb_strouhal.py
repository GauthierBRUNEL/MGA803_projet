import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# 1. Définir le répertoire courant comme celui où se trouve le script
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# 2. Lecture du fichier CSV
#    Adaptez le nom du fichier CSV si nécessaire (ici "monitor.csv")
df = pd.read_csv("monitor.csv")

# 3. Extraction des colonnes
#    Le CSV contient deux colonnes :
#    1) Time
#    2) Max_vitesse_au_point_y Monitor: Max_vitesse_au_point_y Monitor (m/s)
col_time = "Time"
col_vel  = "Max_vitesse_au_point_y Monitor: Max_vitesse_au_point_y Monitor (m/s)"

time = df[col_time].values
velocity = df[col_vel].values

# 4. Plot du signal pour vérifier la nature périodique
plt.figure(figsize=(8,5))
plt.plot(time, velocity, label="Vitesse max point y")
plt.xlabel("Temps (s)")
plt.ylabel("Vitesse (m/s)")
plt.title("Évolution de la vitesse au point y")
plt.grid(True)
plt.legend()
plt.savefig("vitesse_au_point_y.png", dpi=300)
plt.show()

# 5. Détection des pics avec scipy.signal.find_peaks
#    Ajustez 'height' ou d'autres paramètres si nécessaire
peaks, properties = find_peaks(velocity, height=1e-10)  # 'height' = 1e-10 pour ignorer le bruit

peak_times = time[peaks]

# 6. Calcul de la période moyenne
#    On calcule la différence de temps entre pics successifs et on lisse par une moyenne
if len(peak_times) < 2:
    print("Nombre de pics insuffisant pour déterminer la période.")
else:
    dt_peaks = np.diff(peak_times)
    period = np.mean(dt_peaks)
    frequency = 1.0 / period
    
    print(f"Nombre de pics détectés : {len(peaks)}")
    print(f"Période moyenne : {period:.4f} s")
    print(f"Fréquence de détachement (vortex shedding) : {frequency:.4f} Hz")

    # 7. Optionnel : tracé du signal avec les pics identifiés
    plt.figure(figsize=(8,5))
    plt.plot(time, velocity, label="Vitesse max point y")
    plt.plot(peak_times, velocity[peaks], "rx", label="Pics détectés")
    plt.xlabel("Temps (s)")
    plt.ylabel("Vitesse (m/s)")
    plt.title("Détection de pics pour calcul de la période")
    plt.grid(True)
    plt.legend()
    plt.savefig("vitesse_au_point_y_peaks.png", dpi=300)
    plt.show()
