import numpy as np
import pandas as pd
from scipy.spatial import Voronoi, voronoi_plot_2d
from matplotlib import pyplot as plt

df = pd.read_excel('/Users/felipepicard/Documents/01- Fisiologia da Cognição/Experimentos/01 - Mapeamento Motor Callithrix/analise_sitios.xlsx', 'conexões')

# figure scale (set as 1 for arbitrary values)
scale = 1

ri_dict = {}

def calculate_weight(ps, ss):
    # getting the x and y coordinates for the primary and secondary sites
    ps_x = df.iloc[ps, 1]
    ps_y = df.iloc[ps, 2]
    ss_x = df.iloc[ss, 1]
    ss_y = df.iloc[ss, 2]

    ps_pos = np.array((ps_x, ps_y))
    ss_pos = np.array((ss_x, ss_y))

    # calculating the Euclidean distance and multiplying it by the scale factor
    dist = np.linalg.norm (ps_pos - ss_pos) * scale

    return int(dist)

def linear_ri(df):
    for site in range(len(df)):
        









# go through the columns in the dataframe (df)
for site in range(len(df)):
    weight = []
    buffer = []
    # go through the secondary responses for the primary site (sr_ps)
    for response in range(4,8):
        ps_index = site
        sr_ps = df.iloc[site, response]
        #print("Secondary response in primary site: ", sr_ps)
        # for each secondary response, check which other sites have this response as their primary response
        for secondary_site in range(len(df)):
            # if the primary response of the secondary site (pr_ss) is the same as the secondary response in the primary site, calculate the index
            ss_index = secondary_site
            pr_ss = df.iloc[secondary_site, 3]
            if (pr_ss == sr_ps):
                #print("PR_SEC_SITE", site+1, pr_ss)
                #print("SR_PRI_SITE", site+1, sr_ps)
                #print("Primary response in secondary site: ", pr_ss)
                w = calculate_weight(ps_index, ss_index)
                buffer.append(w)
                #print("BUFFER", site+1, buffer)
        #print("NEXT LIMB!!!!")
        # sum all the values in buffer and divide by its length to get the mean weight
        mean_weight = 0
        if (len(buffer) != 0):
            mean_weight = sum(buffer)/len(buffer)
        # add the mean_weight to the weight array
        #print("MEAN WEIGHT", site+1, mean_weight)
        weight.append(mean_weight)
        # free/clear the buffer
        buffer.clear()

    #print("WEIGHT", site+1, weight)
    # sum all the weights in the weight list to calculate the recruitment index (ri)
    ri = sum(weight)
    print("Recruitment Index", site+1, ": ", ri)