# graphic_utils

A repository for utilities related to the visual representation of experimental data.

## Contents
- `voronoi_standalone.py`
- `colorizer.py`

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

## `colorizer.py`

**Objective**  
Generate a color‑coded Voronoi diagram from seed‐point coordinates and a color table stored in an Excel sheet.  

**Usage**  
```bash
python colorizer_script.py path/to/sheet.xlsx output_file_name
```
- path/to/sheet.xlsx – Excel file containing point positions and coloring information.
- output_file_name - Name of the png image generated after the script is run.

**How it works**
1. Read the colorizing_table: the table contains columns for the sites of the voronoi polyhedra, the colors (in RGB) for each site and/or normalized grayscale values (from 0 to 1) as well as the max unnormalized grayscale value. There are also dropdown menus for the kind of colorizing and the positions sheet. More options for these menus can be added in the col_options and pos_options column, respectively.
2. The values in the colorizing_table get stored in a dictionary in the `populate` function.
3. The `colorize` function gets the sites from the positions sheet and colors them with the colors from the colorizer_table. Sites without color entries are interpreted as non-available sites, and get a hash patterning to indicate that.
4. A png image gets generated and saved in the script's folder with the name given in the `output_file_name` field.
 

**Troubleshooting & Notes**
Spreadsheet Path
Ensure the Excel file exists and the path is typed correctly. If the sheet is in the same folder: `python colorizer.py sheet.xlsx output_file_name`. Otherwise, provide the full path:
`python colorizer.py /full/path/to/sheet.xlsx output_file_name`.

Script Path
The code will only run if you are in the folder containing the script (python colorizer.py output_file_name) or if you include the path to the script (python path/to/colorizer.py output_file_name).

Color Modes (in the colorizing_table)
color – uses first RGB entry per site. Invalid/empty cells are interpreted as non-available sites, and are represented as a hatched site in the output image.
grayscale – converts normalized values to gray tones (higher values ➜ darker). Empty cells are also represented as hatched sites in this function.

Style Customization
Color-bar values can be customized by changing relevant lines between 155-165.
Hatching styles can be changed in lines 152-154 and 165-167.
Figure size can be changed in the `figsize` argument in line 114.
