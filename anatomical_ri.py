# import libraries
import numpy as np
import pandas as pd
import colorizer3 as c
from scipy.spatial import Voronoi, voronoi_plot_2d
from matplotlib import pyplot as plt

# TO DO
# insert the anatomical paths from the head to each limb
msc = ['h', 'n', 'sc']
msi = ['h', 'n', 'si']
tron = ['h', 'n', 'sc', 'ti']
mic = ['h', 'n', 't1', 't2', 'ic']
miipsi = ['h', 'n', 't1', 't2', 'ii']
mand = ['md']
ling = ['l']
face = ['f']
mtemp = ['mt']

# TO DO
# insert the anatomical distance in milimeters for each segment
h = 15
n = 13
sc = 45
si = 45
t1 = 56 
t2 = 56
ic = 57
ii = 57
l = 10
f = 10
mt = 10
md = 10

nr = False

def find_segments(response):
    # TO DO:
    # create an empty python list to contain all the segments from the head to the responsive limb
    path = list

    global nr

    # else:
    if response == 'MSC':
        path = msc       
        nr = True 
    if response == 'MSIpsi':
        path = msi
        nr = True

    if response == 'Tron':
        path = tron
        nr = True

    if response == 'MIC':
        path = mic
        nr = True

    if response == 'MIIpsi':
        path = miipsi
        nr = True

    if response == 'Mand':
        path = mand
        nr = True

    if response == 'Ling':
        path = ling
        nr = True

    if response == 'Face':
        path = face
        nr = True
  
    if response == 'Mtemp':
        path = mtemp
        nr = True

    if pd.isna(response) == False:
        
        #print('caminho', response, path)
        return path
    
    else:
        if nr == False:
            #print('no response')
            nr = True
    # if the response is MSC, append the MSC list to the segments list, if the response is MSIpsi, append the MSIpsi list, and so on...

    # return this list
    return

def rindex(sheet_name):
    weights = []
    # go through the rows in the dataframe (df)
    for site in range(len(df)):
        # create empty lists for the buffer and weights
        all_segments = []
        buffer = []
        print("SITE:", df.iloc[site, 0])
        # go through the go through all the motor resposnses generated from this site
        for response in range(3,8):
            # save the current response to the variable res
            res = df.iloc[site, response]

            segments = find_segments(res)
            #print ("SEGMENTS", segments)

            if segments:
                for elementos in segments:
                    buffer.append(elementos)

            #print ("BUFFER", buffer)
            # print("RESPONSE:", res)
            #print("NEXT SITE!!!!")
        global nr 
        nr = False


        # add the segments saved to buffer to the all_segments list
        # usamos o for aqui para tirar o problema de uma lista dentro de uma lista
        for elementos in buffer:
            all_segments.append(elementos)


        # print(all_segments)

        # free/clear the buffer for the next stimulation site
        buffer.clear()

        # TO DO
        # create a list for the filtered_segments
        filtered_segments = []
        # path = []
        for path in all_segments:
            if path not in filtered_segments:
                filtered_segments.append(path)

        print('caminho completo', filtered_segments)
            
            
        # list(set(filtered_segments))
        
        # save each segment in the filtered_segments only once, without repetition

        
        # convert the name of the segments from strings to its anatomical distance. i.e.: 'sc' to 56 cm and save it to the segment_sizes list
        segment_sizes = []
        for elemento in filtered_segments:
            if elemento == 'h':
                segment_sizes.append(h)   

            if elemento == 'n':
                segment_sizes.append(n)  

            if elemento == 'sc':  
                segment_sizes.append(sc)

            if elemento == 'si':  
                segment_sizes.append(si)

            if elemento == 't1':  
                segment_sizes.append(t1)

            if elemento == 't2':  
                segment_sizes.append(t2)

            if elemento == 'ic':  
                segment_sizes.append(ic) 

            if elemento == 'ii':  
                segment_sizes.append(ii)

            if elemento == 'l':  
                segment_sizes.append(l)

            if elemento == 'f':  
                segment_sizes.append(f)

            if elemento == 'mt':  
                segment_sizes.append(mt)

            if elemento == 'md':  
                segment_sizes.append(md)

        # sum the segment sizes and add (append) it to the weights list
        ri = sum(segment_sizes)
        print('tamanho do caminho:',ri)

        weights.append(ri)
        # print the recruitment index with "," instead of "." for decimal places. ex.: 12.5 -> 12,5
        ri_form = str(ri)[:6].replace(".",",")
        print("Recruitment Index", site+1, ": ", ri_form)
        # print(ri_form)

    # convert the weights array to a numpy array so we can work with numpy functions
    weights = np.array(weights)
    # get the maximum value in our array
    v_max = np.max(weights)
    # divide all the items in our array by the max value, so we get a new array whose values range from 0 to 1, and the max value is 1 (max_value/max_value = 1)
    weights = weights/v_max
    print("RECRUITMENT INDEXES:", weights)

    # run the colorize function, that can be found in the colorize3.py file. 
    c.colorize(weights, sheet_name, v_max)

# open dataframe with each muscle from the excel tables
df = pd.read_excel('/Users/felipepicard/Documents/01- Fisiologia da Cognição/Experimentos/01 - Mapeamento Motor Callithrix/analise_sitios.xlsx', 'cabeça')
rindex('FILE_NAME')
