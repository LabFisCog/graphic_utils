import numpy as np
import pandas as pd
from scipy.spatial import Voronoi, voronoi_plot_2d
from matplotlib import pyplot as plt
import teste
import png_maker

df = pd.read_excel('/Users/felipepicard/Documents/01- Fisiologia da Cognição/Experimentos/01 - Mapeamento Motor Callithrix/analise_sitios.xlsx', 'conexões')

scale = 1

points = []
recruitment_index = []

# populate the points array with the positions in the table
for position in range(len(df)):
    pos = []
    pos_x = df.iloc[position, 1]
    pos_y = df.iloc[position, 2]
    pos.append(pos_x)
    pos.append(pos_y)

    points.append(pos)

# populate the recruitment_index (RI) array with the RI's in the table
for ri in range(len(df)):
    rindex = round(df.iloc[ri, 11] / 100, 3)
    recruitment_index.append(rindex)

points = np.array(points)
recruitment_index = np.array(recruitment_index)

vor = Voronoi(points)

# plot
regions, vertices = teste.voronoi_finite_polygons_2d(vor)

current_site = 0


fig, ax = plt.subplots(figsize=(6*1.645, 6*1.135))  # Adjust the width and height as needed

# colorize
for region in regions:
    polygon = vertices[region]
    g = 1 - recruitment_index[current_site]
    ax.fill(*zip(*polygon), facecolor=(g,g,g) , edgecolor='gray', linewidth=1, alpha=0.8)
    current_site = current_site + 1

ax.axis('off')
ax.plot(points[:,0], points[:,1], "o", markersize=4, color="orange", markeredgecolor='black')
plt.xlim(vor.min_bound[0] - 20, vor.max_bound[0] + 20)
plt.ylim(vor.min_bound[1] - 20, vor.max_bound[1] + 20)
plt.savefig("colored_mask.png", bbox_inches='tight')
png_maker.make_png("colored_mask.png")

plt.show()