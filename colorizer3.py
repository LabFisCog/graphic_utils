import numpy as np
import pandas as pd
from scipy.spatial import Voronoi, voronoi_plot_2d
from matplotlib import pyplot as plt
import teste
import png_maker

# # insert the path to your data file
# df = pd.read_excel('/Users/felipepicard/Documents/01- Fisiologia da Cognição/Experimentos/01 - Mapeamento Motor Callithrix/analise_sitios.xlsx', 'dist_cortical')

# scale = 8

# points = []
# recruitment_index = []


def colorize(ri, fname, v_max):
    # insert the path to your data file
    df = pd.read_excel('/Users/felipepicard/Documents/01- Fisiologia da Cognição/Experimentos/01 - Mapeamento Motor Callithrix/analise_sitios.xlsx', 'dist_cortical')

    scale = 8

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
    for rindex in ri:
        recruitment_index.append(rindex)

    points = np.array(points)
    recruitment_index = np.array(recruitment_index)

    vor = Voronoi(points)

    # plot
    regions, vertices = teste.voronoi_finite_polygons_2d(vor)

    current_site = 0


    fig, ax = plt.subplots(figsize=(scale*1.274, scale))  # Adjust the width and height as needed

    # colorize
    for region in regions:
        polygon = vertices[region]
        g = 1 - recruitment_index[current_site]
        if (g == 1):
            ax.fill(*zip(*polygon), facecolor=(1, 1, 0.6235), hatch='////', edgecolor='black', linewidth=1, alpha=1)
        elif (g == -1):
            ax.fill(*zip(*polygon), facecolor='purple' , edgecolor='gray', linewidth=1, alpha=0.2)
        elif (g == -2):
            ax.fill(*zip(*polygon), facecolor='green' , edgecolor='gray', linewidth=1, alpha=0.2)

        else:
            ax.fill(*zip(*polygon), facecolor=(g,g,g) , edgecolor='black', linewidth=1, alpha=1)
        current_site = current_site + 1

    ax.axis('off')
    ax.plot(points[:,0], points[:,1], "o", markersize=4, color="orange", markeredgecolor='black')

    # Create a ScalarMappable object with a grayscale colormap
    cmap = plt.cm.gray_r
    norm = plt.Normalize(vmin=0, vmax=v_max)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])

    # Create an empty Axes object for the colorbar
    fig, ax = plt.subplots(figsize=(2, 8))  # Adjust the width and height as needed

   # Create the colorbar using the ScalarMappable object and the empty Axes
    cb = plt.colorbar(sm, ax=ax, label='IR cortical (U. A.)')
    cb.outline.set_visible(True)  # Optionally, remove the colorbar outline
    plt.axis('off')  # Turn off the axes
    plt.savefig(f"colorbar{fname}.png", bbox_inches='tight', pad_inches=0)  # Adjust pad_inches to control the padding
    plt.close() # Adjust pad_inches to control the padding


    plt.xlim(vor.min_bound[0] - 20, vor.max_bound[0] + 20)
    plt.ylim(vor.min_bound[1] - 20, vor.max_bound[1] + 20)
    plt.savefig(f"{fname}.png", bbox_inches='tight')

    #plt.show()