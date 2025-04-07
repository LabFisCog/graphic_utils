# graphic_utils

a repository for storing the codes used in some visual representation of our experiments' data.

## index
  * voronoi.py

## voronoi.py
objective: create a mesh of voronoi polygons around a group of points in such way that any point within a certain polygon is closest to its seed point than to any other seed point.
usage: ''' python voronoi.py path/to/image.png '''
how it works: takes a source image as an input. The user than selects the points he wants to be used in the voronoi diagram by clicking on them, which will get stored in the 'points' array. This array is used to create a 'Voronoi' object, which than gets turned into a plot and saved as a png with white and transparent background to the user's computer.
troubleshooting:
1- the generated image's dimensions doesn't necessarily match the original image's aspect ratio. I couldn't find a way to fix this in the code, so what I did was to change the aspect ratio manually using some image processing software, than I put this new found aspect ratio into the 'figsize' function at line 95 and multiplied it by a scale factor.
2- the style of the generated plot can be tuned by changing values in the functions from line 100 to 105. 




# graphic_utils

A repository for utilities related to the visual representation of experimental data.

## Contents
- `voronoi.py`

## `voronoi.py`

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
5. The Voronoi diagram is plotted and saved as a PNG file with a white and transparent background.

**Troubleshooting & Notes**

Image Aspect Ratio
The output image may not match the aspect ratio of the original image. To address this:

Adjust the aspect ratio manually using an image processing tool.

Update the figsize parameter at line 95 with the corrected aspect ratio, scaled as needed.

Style Customization
The appearance of the generated plot (colors, line widths, etc.) can be customized by editing the relevant functions between lines 100–105.
