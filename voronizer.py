import numpy as np
import pandas as pd
from scipy.spatial import Voronoi, voronoi_plot_2d
from matplotlib import pyplot as plt
import teste
import png_maker

# insert the path to your data file
df = pd.read_excel('/Users/felipepicard/Documents/01- Fisiologia da Cognição/burish/posicoes_burish.xlsx')

scale = 3

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

points = np.array(points)

vor = Voronoi(points)

# plot
regions, vertices = teste.voronoi_finite_polygons_2d(vor)

current_site = 0


fig, ax = plt.subplots(figsize=(scale, 2.62*scale))  # Adjust the width and height as needed

i = 0

# colorize
for region in regions:
    polygon = vertices[region]

    ax.fill(*zip(*polygon), facecolor='white' , edgecolor='black', linewidth=1, alpha=1)

    current_site = current_site + 1

    i = i+1

ax.axis('off')
ax.plot(points[0:(len(points)-5-1),0], points[0:(len(points)-5-1),1], "o", markersize=4, color="orange", markeredgecolor='black')
ax.plot(points[(len(points)-5):(len(points)),0], points[(len(points)-5):(len(points)),1], "o", markersize=7, color="green", alpha=0.5 , markeredgecolor='black')


plt.xlim(vor.min_bound[0] - 20, vor.max_bound[0] + 20)
plt.ylim(vor.min_bound[1] - 20, vor.max_bound[1] + 20)
plt.savefig("burishzada.png", bbox_inches='tight')
#png_maker.make_png("colored_mask.png")

plt.show()