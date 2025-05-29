# graphic_utils

A repository for utilities related to the visual representation of experimental data.

## Contents
- `voronoi.py`

## `voronoi_standalone.py`

**Objective**  
Generate a mesh of Voronoi polygons around user-defined seed points such that any location within a polygon is closest to its respective seed point.

**Usage**  
```bash
python voronoi.py path/to/image.png
```

**How it works**
1. The script takes an input image.
2. The user manually selects seed points by clicking on the image.
3. Selected points are stored in the points array.
4. A Voronoi object is created using these points.
5. The Voronoi diagram is plotted and saved as a PNG and SVG with an overlay of the original image and the Voronoi diagram.

**Troubleshooting & Notes**
Image Path
If the image path isn't correctly typed, the code may not run. Images (ex.: image.png) on the same folder as the code can be run by typing in the command line: python voronoi.py image.png else, it must include the whole path to the image: python voronoi.py path/to/image.png

Script Path
The code will only run if you are in the folder containing the script (python voronoi.py path/to/image.png) or if you include the path to the script (python path/to/voronoi.py path/to/image.png).

Image Aspect Ratio
The output image may not match the aspect ratio of the original image. To address this:

Adjust the aspect ratio manually using an image processing tool.

Update the figsize parameter at line 95 with the corrected aspect ratio, scaled as needed.

Style Customization
The appearance of the generated plot (colors, line widths, etc.) can be customized by editing the relevant functions between lines 215-220.
The apperance of the SVG file can be changed by altering the background image layer (line 36), the polygons layer (layers 184-189) and the labels layer (lines 192-213). 
