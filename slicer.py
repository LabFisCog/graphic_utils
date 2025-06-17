# slicer
# objective: This code aims to slice a histological section of the cerebral animal cortex. Dividing into small pieces to facilitate later analysis.
# input: An image with the contours for the most external and most internal contours of the cortex;
# output: An image with the cortex and its slices divided by lines. The initial contours given to this code will be preserved in this image.
import numpy as np
import cv2
import sys

up_dataset = [(695, 442), (614, 462), (563, 482), (518, 502), (476, 522), (434, 542), (392, 562), (352, 582), (311, 603), (269, 625), (225, 649), (179, 675), (130, 704), (77, 737), (14, 780), (55, 760), (112, 723), (163, 692), (210, 665), (254, 641), (299, 617), (342, 595), (387, 572), (429, 552), (471, 532), (513, 512), (557, 492), (607, 472), (673, 452), (763, 466), (816, 535), (838, 579), (861, 622), (896, 677), (1016, 707), (1125, 687), (1236, 667), (1362, 704), (1434, 772), (1503, 754), (1547, 732), (1592, 707), (1643, 676), (1694, 645), (1742, 617), (1783, 596), (1829, 573), (1876, 553), (1948, 533), (2155, 517), (2392, 537), (2443, 539), (2260, 519), (1971, 521), (1890, 541), (1838, 561), (1797, 581), (1754, 603), (1709, 628), (1659, 658), (1607, 690), (1559, 718), (1514, 741), (1466, 761), (1392, 731), (1311, 658), (1155, 674), (1060, 694), (925, 695), (871, 627), (846, 581), (822, 533), (772, 465)]
down_dataset = [(672, 1046), (588, 1066), (531, 1086), (483, 1106), (437, 1126), (392, 1147), (348, 1170), (304, 1194), (255, 1223), (202, 1256), (140, 1298), (65, 1353), (46, 1377), (128, 1315), (193, 1270), (247, 1236), (297, 1206), (342, 1181), (386, 1158), (429, 1137), (475, 1117), (521, 1097), (576, 1077), (648, 1057), (745, 1084), (765, 1152), (785, 1247), (808, 1295), (905, 1334), (969, 1314), (1016, 1294), (1059, 1274), (1113, 1254), (1187, 1277), (1239, 1335), (1332, 1331), (1394, 1311), (1453, 1291), (1561, 1279), (1617, 1309), (1679, 1350), (1789, 1352), (1844, 1332), (1901, 1312), (1953, 1292), (1999, 1272), (2046, 1252), (2104, 1232), (2186, 1212), (2382, 1196), (2455, 1216), (2458, 1211), (2384, 1191), (2186, 1205), (2103, 1225), (2045, 1245), (1998, 1265), (1952, 1285), (1900, 1305), (1843, 1325), (1788, 1345), (1687, 1347), (1630, 1312), (1571, 1276), (1459, 1282), (1399, 1302), (1338, 1322), (1247, 1332), (1192, 1272), (1108, 1248), (1056, 1268), (1012, 1288), (966, 1308), (898, 1328), (811, 1287), (789, 1235), (769, 1135), (745, 1071)]

if len(sys.argv) != 3:
        sys.exit("Usage: python slicer.py path/to/image.png number_of_sections")


# save image file-name or path to variable f
f = sys.argv[1]
n_sections = sys.argv[2]

interpoint_distance = 2

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
    
    # # OBS.: talvez seja melhor botar um espaçamento maior entre cada pontinho
    # for contour in up_contour:
    #     for point in contour:
    #         x, y = point[0]
    #         up.append((x,y))
    #         cv2.circle(image, (x, y), 20, (0, 255, 255), -1)


    # for contour in down_contour:
    #      for point in contour:
    #         x, y = point[0]
    #         down.append((x,y))
    #         cv2.circle(image, (x, y), 30, (255, 0, 255), -1)
    if image is None:
         print('Image could not be opened')
   
    # image = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)
    cv2.imshow('exemplo', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
   
    # print("UP!!! ", up)
    # print("\n\n\n")
    # print("DOWN!!!", down)

    # retornar uma lista de tuplas (x, y) para cada contorno ex.: out_cont = [(x1, y1), (x2, y2), (x3, y3)...]
    return up, down


   
def interpolate_contours(contour, n_sections):
    # receives a contour and divides its length by the desired number of sections
    # first, interpolate the curve


    # second, get the length of the curve


    # third, divide the length of the curve by the number of sections


    # fourth, create a list with the points that will be evenly spaced along this curve


    # retornar uma lista com os pontos igualmente espaçados no contorno externo e interno
    return # spaced_points


# OPCIONAL (FAZER POR ULTIMO)
def compute_centerline(outer_contour, inner_contour):
    centerpoints = []
    # gets the outer and inner contour and computes the centerline between them
    for outer_point, inner_point in zip(outer_contour, inner_contour):
        print('outer', outer_point)
        print('inner', inner_point)

        

        center_x = ((outer_point[0] - inner_point[0])/2) + inner_point[0]
        center_y = ((outer_point[1] - inner_point[1])/2) + inner_point[1]
        # centerpoints = np.linalg.norm(outer_array - inner_array)/2

        centerpoint = (center_x, center_y)
        print("centerpoint ", centerpoint)
        centerpoints.append(centerpoint)
        print("centerpoints lista:  ", centerpoints)
        
    return centerpoints

compute_centerline(up_dataset, down_dataset)


def divide_sections(centerline, outer_contour, inner_contour, n_sections):
    # divides the cortex into slices


    return


def visualize(img, outer_points, inner_points):
    # displays the results as an image


    return


get_contours(f)