import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Définir le répertoire courant comme celui du script
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Lecture des fichiers CSV pour chaque maillage
coarse = pd.read_csv("coarse_mesh_velocity_x.csv")
medium = pd.read_csv("medium_mesh_velocity_x.csv")
fine = pd.read_csv("fine_mesh_velocity_x.csv")

# Noms des colonnes tels que définis dans le fichier CSV
col_x = "Line Probe: Direction [1,0,0] (m)"
col_u = "Line Probe: Velocity: Magnitude (m/s)"

# Extraction des données pour chaque maillage
x_coarse = coarse[col_x]
u_coarse = coarse[col_u]
x_medium = medium[col_x]
u_medium = medium[col_u]
x_fine = fine[col_x]
u_fine = fine[col_u]

# Plot comparatif des profils de vitesse axiale u_x
plt.figure(figsize=(10, 6))
plt.plot(x_coarse, u_coarse, label='Coarse mesh (base size = 0.8)', marker='s')
plt.plot(x_medium, u_medium, label='Medium mesh (base size = 0.4)', marker='x')
plt.plot(x_fine, u_fine, label='Fine mesh (base size = 0.2)', marker='o')
plt.xlabel('Position le long de la ligne probe (m)')
plt.ylabel('Vitesse axiale $u_x$ (m/s)')
plt.title('Comparaison des profils de vitesse axiale pour différents maillages')
plt.legend()
plt.grid(True)
plt.savefig("velocity_profiles_comparison.png", dpi=300)
plt.show()

# Calcul des erreurs relatives en pourcentage (référence : maillage fin)
rel_err_coarse = 100 * np.abs(u_coarse - u_fine) / np.abs(u_fine)
rel_err_medium = 100 * np.abs(u_medium - u_fine) / np.abs(u_fine)

# Plot des erreurs relatives en pourcentage
plt.figure(figsize=(10, 6))
plt.plot(x_coarse, rel_err_coarse, label='Erreur relative (Coarse vs Fine)', marker='s')
plt.plot(x_medium, rel_err_medium, label='Erreur relative (Medium vs Fine)', marker='x')
plt.xlabel('Position le long de la ligne probe (m)')
plt.ylabel('Erreur relative (%)')
plt.title('Comparaison des erreurs relatives des profils de vitesse axiale')
plt.legend()
plt.grid(True)
plt.savefig("relative_errors_comparison.png", dpi=300)
plt.show()
