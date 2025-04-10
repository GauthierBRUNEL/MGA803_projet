import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Définir le répertoire courant comme celui du script
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Lecture du fichier CSV
col_x = "Line Probe: Direction [1,0,0] (m)"
col_u = "Line Probe: Velocity: Magnitude (m/s)"
data = pd.read_csv("velocity_x_recirculation.csv")

x = data[col_x].to_numpy()
u = data[col_u].to_numpy()

# Trace du profil de la vitesse longitudinale
plt.figure(figsize=(10, 6))
plt.plot(x, u, marker="o", linestyle="-", color="blue", label="$u_x(x)$")
plt.xlabel("Position \\(x\\) (m)")
plt.ylabel("Vitesse longitudinale \\(u_x\\) (m/s)")
plt.title("Profil de la vitesse longitudinale en fonction de \\(x\\)")
plt.grid(True)
plt.legend()
plt.savefig("velocity_profile.png", dpi=300)
plt.show()

# Définir x = 0.5 comme borne de départ de la zone de recirculation (arête aval)
trailing_edge = 0.5

# Ajouter une marge pour exclure le 1er minimum (par exemple, 0.05 m)
exclusion_margin = 0.05
search_start = trailing_edge + exclusion_margin

# Sélectionner la portion de données pour x >= search_start
mask = x >= search_start
x_region = x[mask]
u_region = u[mask]

# Identifier l'indice du minimum dans u_region
idx_min = np.argmin(u_region)
x_min = x_region[idx_min]
u_min = u_region[idx_min]

# Calcul de la longueur de recirculation : distance entre trailing_edge et ce point
Lr = x_min - trailing_edge
print("Longueur de recirculation : {:.4f} m".format(Lr))

# Tracé du profil avec les deux lignes verticales indiquant trailing_edge et le point minimum
plt.figure(figsize=(10, 6))
plt.plot(x, u, marker="o", linestyle="-", color="blue", label="$u_x(x)$")
plt.axvline(x=trailing_edge, color="green", linestyle="--",
            label="Arête aval: \\(x = {:.2f}\\) m".format(trailing_edge))
plt.axvline(x=x_min, color="red", linestyle="--",
            label="Point minimum: \\(x = {:.4f}\\) m".format(x_min))
plt.xlabel("Position \\(x\\) (m)")
plt.ylabel("Vitesse longitudinale \\(u_x\\) (m/s)")
plt.title("Détermination de la longueur de recirculation")
plt.grid(True)
plt.legend()
plt.savefig("velocity_profile_with_min_and_trailing_edge.png", dpi=300)
plt.show()
