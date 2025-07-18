import sys
import numpy as np
import pandas as pd
from scipy.spatial import Voronoi, voronoi_plot_2d
from matplotlib import pyplot as plt

if len(sys.argv) != 3:
        sys.exit("Usage: python colorizer_script.py path/to/sheet.xlsx output_file_name")

ct = pd.read_excel(sys.argv[1])

data = {
    "site": [],
    "color": [],
    "ri": [],
    "max_val": [],
    "mode": [],
    "position": []
}

# voronoi util to allow us to tweak properties in its regions using matplotlib
def voronoi_finite_polygons_2d(vor, radius=None):
    """
    Reconstruct infinite voronoi regions in a 2D diagram to finite
    regions.

    Parameters
    ----------
    vor : Voronoi
        Input diagram
    radius : float, optional
        Distance to 'points at infinity'.

    Returns
    -------
    regions : list of tuples
        Indices of vertices in each revised Voronoi regions.
    vertices : list of tuples
        Coordinates for revised Voronoi vertices. Same as coordinates
        of input vertices, with 'points at infinity' appended to the
        end.

    """

    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)
    if radius is None:
        radius = np.ptp(vor.points, axis=0).max()

    # Construct a map containing all ridges for a given point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # Reconstruct infinite regions
    for p1, region in enumerate(vor.point_region):
        vertices = vor.regions[region]

        if all(v >= 0 for v in vertices):
            # finite region
            new_regions.append(vertices)
            continue

        # reconstruct a non-finite region
        ridges = all_ridges[p1]
        new_region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # finite ridge: already in the region
                continue

            # Compute the missing endpoint of an infinite ridge

            t = vor.points[p2] - vor.points[p1] # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        # sort region counterclockwise
        vs = np.asarray([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:,1] - c[1], vs[:,0] - c[0])
        new_region = np.array(new_region)[np.argsort(angles)]

        # finish
        new_regions.append(new_region.tolist())

    return new_regions, np.asarray(new_vertices)


def populate_data(ct):
    # populate the data dictionary
    for row in range(len(ct)):
        site = ct.iloc[row, 0]
        ri = ct.iloc[row, 6]
        max_val = ct.iloc[0, 7]
        mode = ct.iloc[0, 9]
        position = ct.iloc[0, 10]
        color = []
        # populate the color list with as many colors as there are in the sheet for that specific row
        for col in range(1, 6):  # Iterate over columns 1 to 5
            current_color = ct.iloc[row, col]
            if pd.isna(current_color):  # Stop if cell is empty
                break
            color.append(current_color)
        # populate the data dictionary
        data["site"].append(site)
        data["color"].append(color)
        data["ri"].append(ri)
        data["max_val"].append(max_val)
        data["mode"].append(mode)
        data["position"].append(position)

    # print(data)

populate_data(ct)



def grayscale(index):
    color = [1, 0, 1]
    hatch = '////'
    gray = 0
    
    if pd.isna(data["ri"][index]):
        color = [1, 1, 0.6235]
        hatch = '////'

    else:
        gray = 1 - data["ri"][index]
        color = [gray, gray, gray]
        hatch = None

    return color, hatch

def colors(index):
    color = [1, 0, 1]
    hatch = '////'
    first_color = color

    color_data = data["color"][index]

    if not pd.isna(color_data).all():
        first_color = color_data[0]
        rgb_array = [int(value.strip()) for value in first_color.split(',')]
        color = np.array(rgb_array) / 255
        hatch = None

    else:
        color = [1, 0, 1]
        hatch = '////'
    
    return color, hatch


def colorize(data, fname, v_max):
    # insert the path to your data file
    df = pd.read_excel(data["position"][0])

    scale = 8
    points = []

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

    # generate regions
    regions, vertices = voronoi_finite_polygons_2d(vor)

    fig, ax = plt.subplots(figsize=(scale*1.274, scale))  # Adjust the width and height as needed

    # colorize
    for index, region in enumerate(regions):
        color = np.array([0,0,0])
        hatch = None
        polygon = vertices[region]

        print(data["mode"][index])
        if data["mode"][index] == "grayscale":
            color, hatch = grayscale(index)

        if data["mode"][index] == "color":
            color, hatch = colors(index)

        ax.fill(*zip(*polygon), facecolor=color, hatch=hatch, edgecolor='black', linewidth=1, alpha=1)

        # print("region", index)

    ax.axis('off')
    ax.plot(points[:,0], points[:,1], "o", markersize=4, color="orange", markeredgecolor='black')

    if data["mode"][0] == "grayscale":
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
        plt.savefig(f"colorbar_{fname}.png", bbox_inches='tight', pad_inches=0)  # Adjust pad_inches to control the padding
        plt.close() # Adjust pad_inches to control the padding

    plt.xlim(vor.min_bound[0] - 20, vor.max_bound[0] + 20)
    plt.ylim(vor.min_bound[1] - 20, vor.max_bound[1] + 20)
    plt.savefig(f"{fname}.png", bbox_inches='tight')

    plt.show()

colorize(data, sys.argv[2], data["max_val"][0])