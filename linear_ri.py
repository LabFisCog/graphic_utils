import numpy as np
import pandas as pd
from math import sqrt
from scipy.spatial import Voronoi, voronoi_plot_2d
from matplotlib import pyplot as plt
# import colorizer3 as c

# open dataframe
df_general = pd.read_excel('dados.xlsx', 'Sheet1_geral')
df_cs01 = pd.read_excel('dados.xlsx', 'Sheet2_ld')

# figure scale (set as 1 for arbitrary values)
scale = 1

ri_array = []
get_mean_of_representations = False
normalize_irm = False

cc_x = float(df_general.iloc[0, 9])
cc_y = float(df_general.iloc[1, 9])
print("CC_x = ", cc_x)
print("CC_y = ", cc_y)

def calculate_weight(ps, ss, ipsi=False):
    # getting the x and y coordinates for the primary and secondary sites
    ps_x = float(df_cs01.iloc[ps, 0])
    ss_x = float(df_general.iloc[ss, 0])

    psite = np.array((ps_x, 0))
    ssite = np.array((ss_x, 0))
    cc = np.array((cc_x, cc_y))

    dist_ipsi = 0

    # print(f"Primary site {ps+1} position: ", ps_x)
    # print(f"Secondary site {ss+1} position: ", ss_x)
    if ipsi == True:
        dist = (np.linalg.norm(psite - cc) + np.linalg.norm(cc - ssite)) * scale
        print("dist ipsi = ", dist_ipsi)

    else:
        # calculating the Euclidean distance and multiplying it by the scale factor
        dist = dist_ipsi + (sqrt((ps_x - ss_x)**2) * scale)

    return float(dist)

# go through the columns in the dataframe (df)
for site in range(len(df_cs01)):
    weight = []
    buffer = []
    ps_index = site
    # go through the responses for the primary site (r_ps)
    for response in range(1,5):
        # initialize ipsi as false since most sites are only contralateral
        ipsi = False
        resp_ps = df_cs01.iloc[site, response]
        # check if it is ipsilateral
        if isinstance(resp_ps, str) and resp_ps.startswith('i'):
            print("ipsi response: ", resp_ps)
            resp_ps = resp_ps[1:]
            ipsi = True
            # print("Secondary response in primary site: ", sr_ps)
            # for each secondary response, check which other sites have this response as their primary response
        for secondary_site in range(len(df_general)):
            for response in range (1, 6):
                ss_index = secondary_site
                resp_ss = df_general.iloc[secondary_site, response]
                if isinstance(resp_ps, str) and resp_ps == resp_ss:
                    w = calculate_weight(ps_index, ss_index, ipsi)
                    buffer.append(w)
                    ipsi = False

        new_weight = 0
        if get_mean_of_representations == True:
            if (len(buffer) != 0):
                new_weight = sum(buffer)/len(buffer)
        else:
            new_weight = sum(buffer)
        weight.append(new_weight)
        buffer.clear()

    ri = sum(weight)
    ri_array.append(ri)
    ri_form = str(ri)[:6].replace(".",",")
    # print("Recruitment Index", site+1, ": ", ri)
    print("Recruitment Index", site+1, ": ", ri_form)
    

# print("WEIGHT", site+1, weight)

ri_array = np.array(ri_array)

if normalize_irm == True:
    print("Max val = ", np.max(ri_array))
    ri_array = ri_array/(np.max(ri_array))
print("Recruitment index array: ", ri_array)

# c.colorize(ri_array, "ri_penfield")