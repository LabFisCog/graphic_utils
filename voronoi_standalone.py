import pygame
import sys
import numpy as np
from scipy.spatial import Voronoi
from matplotlib import pyplot as plt
import cv2
import svgwrite

# this program allows the user to select multiple points in an image and automatically creates
# a voronoi diagram for the selected group of points. The script saves the resulting diagram
# both as a PNG image as well as an SVG with layers for the template image, the voronoi diagram itself
# as well as the selected dots with numbered labels on top.

# usage: in the command line type: python voronoi.py path/to/image.png
# if your image is in the same folder as the script, you can open the command line at this folder and just
# type python voronoi.py image.png  . The program will open your image and you must click the points you
# want displayed in your voronoi diagram. After selecting all the point, just press Enter. The program will
# automatically save the images with the name "output_voronoi" as a png and svg. Have fun!

if len(sys.argv) != 2:
    sys.exit("Usage: python voronoi.py path/to/image.png")

f = sys.argv[1]
# gets the image dimensions
img = cv2.imread(f)
height, width, _ = img.shape

# converts the image to pygame coordinates and color schemes
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_surface = pygame.image.frombuffer(img_rgb.tobytes(), (width, height), 'RGB')

# creates SVG file
dwg = svgwrite.Drawing('output_voronoi.svg', size=(width, height))

# layer 1 - background image
dwg.add(dwg.image(href=f, insert=(0, 0), size=(width, height)))

# initialize pygame
pygame.init()
displaysurface = pygame.display.set_mode((width, height))
pygame.display.set_caption("Image")

# variables for storing the group of dots
points = []
previous_release = True

def get_points():
    global previous_release
    m_left, _, _ = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    # save the current mouse position if left mouse button is clicked
    if m_left and previous_release:
        pos = (x, y) 
        print(pos)
        points.append(pos)
        previous_release = False
    if not m_left:
        previous_release = True

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

# run the clicking point selector until pygame is closed or user hits Enter (return) or Escape 
run = True
while run:
    displaysurface.blit(img_surface, (0, 0))  # uses the image converted by opencv
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or key[pygame.K_RETURN] or key[pygame.K_ESCAPE]:
            run = False
    get_points()
    pygame.display.flip()

# remove duplicates and convert to np.array so we can plot it
points = list(dict.fromkeys(points))
points = np.array(points)
print("Voronoi polyhedra points: ", points)

if len(points) < 3:
    sys.exit("Erro: Você precisa selecionar pelo menos 3 pontos para criar um Voronoi.")

vor = Voronoi(points)
regions, vertices = voronoi_finite_polygons_2d(vor)
voronoi_layer = dwg.add(dwg.g(id='voronoi_layer'))

# define plot dimensions to be the same as the original image
dpi = 100
fig_width = width / dpi
fig_height = height / dpi

fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=dpi)
ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  # includes original image as background of the plot
ax.set_xlim(0, width)
ax.set_ylim(height, 0)
ax.set_aspect('equal')
ax.axis('off')

# draw lines between the voronoi regions
# layer 2 - save the polygons in a new layer
for region in regions:
    polygon = vertices[region]
    ax.fill(*zip(*polygon), facecolor='none', edgecolor='gray', linewidth=1, alpha=0.8)
    voronoi_layer.add(dwg.polygon(
        points=[(x, y) for x, y in polygon],
        fill='none',
        stroke='gray',
        stroke_width=1
    ))

# layer 3 - dots and labels
points_layer = dwg.add(dwg.g(id='points_layer'))
for idx, (x, y) in enumerate(points):
    x = float(x)
    y = float(y)
    # orange circle in selected point
    points_layer.add(dwg.circle(center=(x, y), r=5, fill='orange', stroke='black', stroke_width=1))
    
    num_radius = 10
    cx_num = x + 10
    cy_num = y - num_radius - 5
    points_layer.add(dwg.circle(center=(cx_num, cy_num), r=num_radius, fill='white', stroke='black', stroke_width=1))
    
    # Center text/label in a white circle
    points_layer.add(dwg.text(
        str(idx + 1),
        insert=(cx_num, cy_num + 4),  # in "cy_num + n", n can be changed to adjust vertically
        text_anchor="middle",
        font_size='14px',
        fill='black',
        alignment_baseline="middle",
        font_family="Times New Roman" # define font (your PC must have the selected font already installed)
    ))


ax.plot(points[:,0], points[:,1], "o", markersize=4, color="orange", markeredgecolor='black')

# save the generated files
voronoi_filename = "output_voronoi.png"
plt.savefig(voronoi_filename, bbox_inches=None, pad_inches=0)
plt.close()

print("Voronoi salvo como mask.png")

dwg.save()
print("SVG saved as output_voronoi.svg")