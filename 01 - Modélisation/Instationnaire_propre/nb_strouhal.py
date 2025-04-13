import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Définir le répertoire courant comme celui où se trouve le script
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Répertoire d'entrée contenant les fichiers CSV
data_folder = "data"

# Listes des valeurs de Re et D à traiter (pour les simulations instationnaires, Re > 10)
Re_list = [200, 500, 1000]
D_list = [1, 1.5, 2.5]

# Paramètres physiques pour l'air
mu = 1.8e-5      # viscosité dynamique en Pa·s (m²/s)
rho = 1.225      # masse volumique en kg/m³

# Chemin du fichier CSV de sortie pour les résultats (dans le dossier data)
output_csv = os.path.join(data_folder, "resultats_strouhal.csv")

# Liste pour stocker les résultats sous forme de dictionnaires
resultats = []

# Itération sur toutes les combinaisons Re et D
for Re_val in Re_list:
    for D_val in D_list:
        # Construction du nom du fichier CSV, ex: "Max_V_sur_Y_Re200_D1.csv"
        filename = f"Max_V_sur_Y_Re{Re_val}_D{D_val}.csv"
        filepath = os.path.join(data_folder, filename)
        if not os.path.exists(filepath):
            print(f"=======================================================")
            print(f"Fichier {filepath} non trouvé, passage.")
            continue

        print(f"=======================================================")
        print(f"Traitement de {filepath} : Re = {Re_val}, D = {D_val} m")
        
        # Calcul de la vitesse libre U0 : U0 = (Re * mu) / (rho * D)
        U0 = Re_val * mu / (rho * D_val)
        print(f"  U0 = {U0:.4f} m/s")
        
        # Lecture du fichier CSV
        df = pd.read_csv(filepath)
        col_time = "Time"
        col_vel  = "Max_vitesse_au_point_y Monitor: Max_vitesse_au_point_y Monitor (m/s)"
        time = df[col_time].values
        velocity = df[col_vel].values
        
        # Optionnel : Tracé du signal complet
        plt.figure(figsize=(8,5))
        plt.plot(time, velocity, label="Vitesse max point y")
        plt.xlabel("Temps (s)")
        plt.ylabel("Vitesse (m/s)")
        plt.title(f"Évolution de la vitesse au point y - {filename}")
        plt.grid(True)
        plt.legend()
        plot_filename = os.path.join(data_folder, f"vitesse_au_point_y_{Re_val}_{D_val}.png")
        plt.savefig(plot_filename, dpi=300)
        plt.close()
        
        # Détection des pics dans le signal
        peaks, properties = find_peaks(velocity, prominence=1e-12)
        peak_times = time[peaks]
        
        if len(peak_times) < 4:
            print(f"  Nombre de pics insuffisant dans {filename} pour déterminer la périodicité.")
            continue
        else:
            # Utiliser les 4 derniers pics (3 intervalles) pour isoler la phase bien périodique
            last_peak_times = peak_times[-4:]
            dt_peaks = np.diff(last_peak_times)
            period = np.mean(dt_peaks)
            frequency = 1.0 / period
            
            print(f"  Période moyenne (3 derniers intervalles) : {period:.4f} s")
            print(f"  Fréquence moyenne : {frequency:.4f} Hz")
            
            # Calcul du nombre de Strouhal : St = (f * D) / U0
            St = frequency * D_val / U0
            print(f"  Nombre de Strouhal (St) : {St:.4f}")
            
            # Optionnel : Tracé du signal avec les pics détectés
            plt.figure(figsize=(8,5))
            plt.plot(time, velocity, label="Vitesse max point y")
            plt.plot(peak_times, velocity[peaks], "rx", label="Pics détectés")
            plt.xlabel("Temps (s)")
            plt.ylabel("Vitesse (m/s)")
            plt.title(f"Détection de pics - {filename}")
            plt.grid(True)
            plt.legend()
            peaks_plot_filename = os.path.join(data_folder, f"vitesse_au_point_y_peaks_{Re_val}_{D_val}.png")
            plt.savefig(peaks_plot_filename, dpi=300)
            plt.close()
            
            resultats.append({
                "Filename": filename,
                "Re": Re_val,
                "D": D_val,
                "U0 (m/s)": U0,
                "Période moyenne (s)": period,
                "Fréquence (Hz)": frequency,
                "St": St
            })

# Conversion des résultats en DataFrame et sauvegarde dans un fichier CSV
df_resultats = pd.DataFrame(resultats)
df_resultats.to_csv(output_csv, index=False)
print(f"Résultats sauvegardés dans {output_csv}")

# 9. Comparaison : tracé de St en fonction de Re pour chaque valeur de D
plt.figure(figsize=(8,5))
for D_val in sorted(df_resultats["D"].unique()):
    subset = df_resultats[df_resultats["D"] == D_val]
    plt.plot(subset["Re"], subset["St"], marker="o", linestyle="-", label=f"D = {D_val} m")
plt.xlabel("Reynolds")
plt.ylabel("Nombre de Strouhal (St)")
plt.title("Comparaison de St en fonction du Re pour différentes valeurs de D")
plt.grid(True)
plt.legend()
plot_comp_filename = os.path.join(data_folder, "St_vs_Re.png")
plt.savefig(plot_comp_filename, dpi=300)
plt.close()
print(f"Graphique de comparaison St vs Re sauvegardé dans {plot_comp_filename}")
