# slicer
# objective: This code aims to slice a histological section of the cerebral animal cortex. Dividing into small pieces to facilitate later analysis.
# input: An image with the contours for the most external and most internal contours of the cortex;
# output: An image with the cortex and its slices divided by lines. The initial contours given to this code will be preserved in this image.
import numpy as np
import cv2
import sys
import os
from scipy.interpolate import interp1d, CubicSpline
import matplotlib.pyplot as plt

if len(sys.argv) != 3:
        sys.exit("Usage: python slicer.py path/to/image.png number_of_sections")


# save image file-name or path to variable f
f = sys.argv[1]
n_sections = int(sys.argv[2])

interpoint_distance = 20
dist_threshold = 10
resolution = 600
offset = 10

def get_contours(img):
    # gets the image and extracts the points from the outter and inner contours
    image = cv2.imread(img)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


    # Define the color range from the lines
    up_color = cv2.inRange(image, (0, 70, 50), (10, 255, 255)) # Podemos, posteriormente colocar um dict com presets de cores pro usuário escolher qual cor é qual camada.
    down_color = cv2.inRange(image, (40, 70, 50), (80, 255, 255))


    # Capture the contours of each line
    up_contour, _ = cv2.findContours(up_color, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    down_contour, _ = cv2.findContours(down_color, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    up = []
    down = []

    for contour in up_contour:
        for i in range(0, len(contour), interpoint_distance):  # <-- Pula de 10 em 10 pontos
            x, y = contour[i][0]
            up.append((x, y))
            cv2.circle(image, (x, y), 10, (0, 255, 255), -1)

    for contour in down_contour:
        for i in range(0, len(contour), interpoint_distance):  # <-- Mesmo aqui
            x, y = contour[i][0]
            down.append((x, y))
            cv2.circle(image, (x, y), 10, (255, 0, 255), -1)
    
    if image is None:
         print('Image could not be opened')
   
    # image = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)
    # cv2.imshow('exemplo', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    up = np.array(up)
    down = np.array(down)

    up = up[np.argsort(up[:, 0])]
    down = down[np.argsort(down[:, 0])]
    # print("UP!!! ", up)
    # print("\n\n\n")
    # print("DOWN!!!", down)

    # retornar uma lista de tuplas (x, y) para cada contorno ex.: out_cont = [(x1, y1), (x2, y2), (x3, y3)...]
    return up, down


   
def interpolate_contours(contour, resolution, n_sections):
    # receives a contour and divides its length by the desired number of sections
    # first, interpolate the curve
    points = np.array(contour)

    # second, get the length of the curve
    # Parametriza por comprimento de arco
    dists = np.sqrt(np.sum(np.diff(points, axis=0)**2, axis=1))
    t = np.concatenate(([0], np.cumsum(dists)))  # comprimento acumulado
    if len(t) != len(points):
        raise ValueError("Número de parâmetros t não bate com número de pontos")

    # Interpola x(t) e y(t)
    cs_x = CubicSpline(t, points[:, 0])
    cs_y = CubicSpline(t, points[:, 1])

    # third, divide the length of the curve by the number of sections
    t_new = np.linspace(0, t[-1], n_sections)
    x_new = cs_x(t_new)
    y_new = cs_y(t_new)


    # fourth, create and return a list with the points that will be evenly spaced along this curve
    return np.stack((x_new, y_new), axis=1)


# OPCIONAL (FAZER POR ULTIMO)
def compute_centerline(outer_contour, inner_contour):
    centerpoints = []
    # gets the outer and inner contour and computes the centerline between them
    for outer_point, inner_point in zip(outer_contour, inner_contour):
        # print('outer', outer_point)
        # print('inner', inner_point)

        

        center_x = ((outer_point[0] - inner_point[0])/2) + inner_point[0]
        center_y = ((outer_point[1] - inner_point[1])/2) + inner_point[1]
        # centerpoints = np.linalg.norm(outer_array - inner_array)/2

        centerpoint = (center_x, center_y)
        # print("centerpoint ", centerpoint)
        centerpoints.append(centerpoint)
        # print("centerpoints lista:  ", centerpoints)
        
    return centerpoints




def divide_sections(centerline, outer_contour, inner_contour, n_sections):
    # divides the cortex into slices


    return


def visualize(img, upper_points, lower_points):
    # displays the results as an image
    image = cv2.imread(img)
    height, width = image.shape[:2]
    output_path = "output_slices_folder"

    os.makedirs(output_path, exist_ok=True)

    sections = []

    for i in range (1, len(upper_points)):
        # section's upper points
        pu1 = upper_points[i-1]
        pu2 = upper_points[i]

        # section's lower points
        pl1 = lower_points[i-1]
        pl2 = lower_points[i]

        # apply an offset
        pu1[1] -= offset
        pu2[1] -= offset
        pl1[1] += offset
        pl2[1] += offset


        polygon = np.array([[pu1, pu2, pl2, pl1]], dtype=np.int32)
    
        mask = np.zeros((height, width, 3), dtype=np.uint8)

        cv2.fillPoly(mask, polygon, (255, 255, 255))

        # draw colored border on the polygon
        cv2.polylines(mask, polygon, isClosed=True, color=(255, 0, 255), thickness=2)

        masked_section = cv2.bitwise_and(image, mask)

        sections.append(masked_section)

    for i, masked_img in enumerate(sections):
        filename = os.path.join(output_path, f"section_{i:02d}.png")
        cv2.imwrite(filename, masked_img)

    return


up_c, dw_c = get_contours(f)

# print("TAMANHO UPPER", len(up_c))
# print("TAMANHO LOWER", len(dw_c))

centerline = compute_centerline(up_c, dw_c)

spaced_up = interpolate_contours(up_c, resolution, n_sections)
spaced_down = interpolate_contours(dw_c, resolution, n_sections)
spaced_cl = interpolate_contours(centerline, resolution, n_sections)

# Visualização
plt.figure(figsize=(8, 6))
original_points_np_up = np.array(up_c)
original_points_np_down = np.array(dw_c)
xs = (0, 100, 1)
plt.plot(original_points_np_up[:, 0], original_points_np_up[:, 1], 'ro-', markersize=3, label='Originais_upper')
plt.plot(original_points_np_down[:, 0], original_points_np_down[:, 1], 'go-', markersize=3, label='Originais_lower')

# Plota as linhas que conectam os pares
for p_up, p_down in zip(spaced_up, spaced_down):
    x_vals = [p_up[0], p_down[0]]
    y_vals = [p_up[1], p_down[1]]
    plt.plot(x_vals, y_vals, color='blue')

plt.plot(spaced_up[:, 0], spaced_up[:, 1], 'bo', markersize=8, label='Interpolados_upper')
plt.plot(spaced_down[:, 0], spaced_down[:, 1], 'bo', markersize=8, label='Interpolados_lower')
plt.plot(spaced_cl[:, 0], spaced_cl[:, 1], 'ro-', markersize=2, label='Interpolados_cl')

plt.legend()
plt.title("Interpolação de Contorno")
plt.axis('equal')
plt.grid(True)
plt.show()

visualize(f, spaced_up, spaced_down)