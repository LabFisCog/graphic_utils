import pygame
import sys
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
from matplotlib import pyplot as plt
import cv2
import png_maker

# voronoi points array
points = []

# include your screen height (in pixels) and DPI
scr_h = 956
dpi = 84

if len(sys.argv) != 2:
        sys.exit("Usage: python voronoi.py path/to/image.png")

# save image file-name or path to variable f
f = sys.argv[1]

# open image
img = cv2.imread(f)

# get width and height (in pixels)
height, width, _ = img.shape

pygame.init()
HEIGHT = height
WIDTH = width
FPS = 30

print(WIDTH)
print(HEIGHT)

previous_release = True

# create canvas
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Image")
bg = pygame.image.load(f)

def get_points():
        global previous_release
        m_left, _, _ = pygame.mouse.get_pressed()
        x, y = pygame.mouse.get_pos()

        if m_left == True and previous_release == True:
                pos = (x, scr_h-y)
                print(pos)
                points.append(pos)
                previous_release = False

        if m_left == False:
               previous_release = True
               


# run display loop
run = True
while run:
        # set background image
        displaysurface.blit(bg, (0, 0))

        key = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or key[pygame.K_RETURN] == True or key[pygame.K_ESCAPE] == True:
                   run = False

        get_points()
        #print(key)

        # flip from memory screen to visible screen
        pygame.display.flip()
        

# remove duplicates
points = list(dict.fromkeys(points))

points = np.array(points)

print("Voronoi polyhedra points: ", points)

# populate scatter plot with points
#plt.scatter(points[:,0], points[:,1])

# create voronoi object
vor = Voronoi(points)

# get vertices
vor_vertices = vor.vertices

# create regions
vor_regions = vor.regions

fig = voronoi_plot_2d(vor, ax = None, show_vertices = False, line_width = 2, line_alpha = 0.2, linestyle='solid')

# fig.set_figwidth(WIDTH/dpi)
# fig.set_figheight(HEIGHT/dpi)

fig.set_figwidth(6*1.645)
fig.set_figheight(6*1.135)

#plt.axis('off')
plt.savefig("mask.png", bbox_inches='tight')
png_maker.make_png("mask.png")
plt.show()