import numpy as np
import pandas as pd
from scipy.spatial import Voronoi, voronoi_plot_2d
from matplotlib import pyplot as plt
import teste

# # insert the path to your data file
# df = pd.read_excel('/Users/felipepicard/Documents/01- Fisiologia da Cognição/Experimentos/01 - Mapeamento Motor Callithrix/analise_sitios.xlsx', 'dist_cortical')

# scale = 8

# points = []
# recruitment_index = []


def colorize(data, fname, v_max):
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

    points = np.array(points)

    vor = Voronoi(points)

    # plot
    regions, vertices = teste.voronoi_finite_polygons_2d(vor)

    current_site = 0


    fig, ax = plt.subplots(figsize=(scale*1.274, scale))  # Adjust the width and height as needed

    # colorize
    i = 1
    l = 0
    for region in regions:
        polygon = vertices[region]
        print("i", i)
        #print("l", (data["site"][l]))

        if l < 29:
            if i == 10:
                print("TESTE")
                color = np.array(data["color"][0])/255
                ax.fill(*zip(*polygon), facecolor=color , edgecolor='black', linewidth=1, alpha=1)

            if i == data["site"][l]:
                color = np.array(data["color"][l])/255
                print(color)
                # if (g == 1):
                #     ax.fill(*zip(*polygon), facecolor=(1, 1, 0.6235), hatch='////', edgecolor='black', linewidth=1, alpha=1)
                # elif (g == -1):
                #     ax.fill(*zip(*polygon), facecolor='purple' , edgecolor='black', linewidth=1, alpha=0.2)
                # elif (g == -2):
                #     ax.fill(*zip(*polygon), facecolor='green' , edgecolor='black', linewidth=1, alpha=0.2)
                # # colorize according to the recruitment index
                # else:
                ax.fill(*zip(*polygon), facecolor=color , edgecolor='black', linewidth=1, alpha=1)
                l += 1

            else:
                if i != 10:
                    print("AAAA")
                    ax.fill(*zip(*polygon), facecolor='white', hatch='////', edgecolor='black', linewidth=1, alpha=1)

        else:
            print("AAAA")
            ax.fill(*zip(*polygon), facecolor='white', hatch='////', edgecolor='black', linewidth=1, alpha=1)
            
        i += 1

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
    cb = plt.colorbar(sm, ax=ax, label='IR cort+baseline (U. A.)')
    cb.outline.set_visible(True)  # Optionally, remove the colorbar outline
    plt.axis('off')  # Turn off the axes
    plt.savefig(f"colorbar{fname}.png", bbox_inches='tight', pad_inches=0)  # Adjust pad_inches to control the padding
    plt.close() # Adjust pad_inches to control the padding


    plt.xlim(vor.min_bound[0] - 20, vor.max_bound[0] + 20)
    plt.ylim(vor.min_bound[1] - 20, vor.max_bound[1] + 20)
    plt.savefig(f"{fname}.png", bbox_inches='tight')

    plt.show()

# IR por número de membros recrutados
initial_membros = {
    "site" : [1, 2, 3, 4 , 11,12,13,14,15,16,17,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37],
    "ri" : [0.286, 0.143, 0.143, 0.429, 0.143, 0.143, 0.286, 0.4, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.333, 0.3333, 0.333, 0.5, 0.5, 0.5]
}

final_membros = {
    "site" : [1, 2, 3, 4 , 11,12,13,14,15,16,17,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37],
    "ri" : [0.714, 1, 0.714, 0.429, 0.714, 0.286, 1, 0.4, 0.2, 0.2, 0.2, 0.2, 0.4, 0.4, 0.6, 1, 0.8, 0.2, 0.6, 0.4, 1, 0.2, 0.2, 1, 0.667, 1, 1, 1, 1, 1]
}


# IR por distância anatômica a partir da cabeça
initial_head = {
    "site" : [1, 2, 3, 4, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37],
    "ri" : [0.395, 0.224, 0.224, 1, 0.224, 0.224, 0.278, 0.067, 0.033, 0.033, 0.033, 0.244, 0.244, 0.244, 0.067, 0.033, 0.244, 0.244, 0.244, 0.033, 0.244, 0.033, 0.244, 0.033, 0.033, 0.033, 0.033, 0.033, 0.033]
}

final_head = {
    "site" : [1, 2, 3, 4, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37],
    "ri" : [1, 1, 1, 0.869, 1, 0.343, 0.328, 0.058, 0.029, 0.029, 0.029, 0.343, 0.343, 0.343, 0.401, 0.087, 0.212, 0.241, 0.241, 0.241, 0.212, 0.029, 0.401, 0.241, 0.27, 0.087, 0.058, 0.058, 0.058]
}


# IR por distância anatômica a partir do centro de massa
initial_cm = {
    "site" : [1, 2, 3, 4, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37],
    "ri" : [0.462, 0.32, 0.32, 0.538, 0.32, 0.32, 0.392, 0.25, 0.177, 0.177, 0.177, 0.32, 0.32, 0.32, 0.25, 0.25, 0.32, 0.32, 0.32, 0.25, 0.32, 0.177, 0.32, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]
}

final_cm = {
    "site" : [1, 2, 3, 4, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37],
    "ri" : [1, 1, 1, 0.538, 1, 0.462, 0.456, 0.25, 0.177, 0.177, 0.177, 0.462, 0.462, 0.462, 0.535, 0.282, 0.32, 0.392, 0.392, 0.392, 0.32, 0.177, 0.535, 0.392, 0.392, 0.282, 0.25, 0.25, 0.25]
}

# IR por distância cortical das representações dos membros a partir do sítio de microestimulação
initial_cort = {
    "site" : [1, 2, 3, 4, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37],
    "ri" : []
}

final_cort = {
    "site" : [1, 2, 3, 4, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37],
    "ri" : []
}

initial_cort_baseline = {
    "site" : [1, 2, 3, 4, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37],
    "ri" : [0.071, 0.071, 0.071, 0.071, 0.071, 0.071, 0.293, 0.303, 0.071, 0.071, 0.071, 0.071, 0.071, 0.071, 0.193, 0.071, 0.071, 0.071, 0.071, 0.071, 0.071, 0.071, 0.071, 0.071, 0.071, 0.071, 0.071, 0.071, 0.071]
}

final_cort_baseline = {
    "site" : [1, 2, 3, 4, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37],
    "ri" : [0.354, 0.27, 0.165, 0.071, 0.357, 0.071, 1, 0.342, 0.071, 0.071, 0.071, 0.071, 0.071, 0.071, 0.524, 0.367, 0.071, 0.173, 0.143, 0.317, 0.071, 0.071, 0.531, 0.25, 0.53, 0.388, 0.285, 0.522, 0.477]
}

membros = {
    "site" : [1, 2, 3, 4, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37],
    "color" : [(117, 215, 255), (117, 215, 255), (117, 215, 255), (33, 92, 153), (117, 215, 255), (117, 215, 255), (117, 215, 255), (193, 232, 114), (193, 232, 114), (193, 232, 114), (193, 232, 114), (117, 215, 255), (117, 215, 255), (117, 215, 255), (255, 138, 216), (148, 22, 81), (117, 215, 255), (117, 215, 255), (117, 215, 255), (255, 138, 216), (117, 215, 255), (193, 232, 114), (117, 215, 255), (255, 138, 216), (255, 138, 216), (146, 146, 146), (146, 146, 146), (146, 146, 146), (146, 146, 146)]
}

colorize(membros, "colors", 1256)