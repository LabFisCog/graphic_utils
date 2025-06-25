import numpy as np
import pandas as pd
from scipy.spatial import Voronoi, voronoi_plot_2d
from matplotlib import pyplot as plt
import colorizer3 as c

# open dataframe
df = pd.read_excel('/Users/felipepicard/Documents/01- Fisiologia da Cognição/Experimentos/01 - Mapeamento Motor Callithrix/analise_sitios.xlsx', 'dist_cortical')

# figure scale (set as 1 for arbitrary values)
scale = 1

ri_array = []
get_mean_of_representations = True

def calculate_weight(ps, ss, ipsi=False):
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

# go through the columns in the dataframe (df)
for site in range(len(df)):
    weight = []
    buffer = []
    ps_index = site
    # go through the responses for the primary site (r_ps)
    for response in range(4,8):
        # initialize ipsi as false since most sites are only contralateral
        ipsi = False
        resp_ps = df.iloc[site, response]
        # check if it is ipsilateral
        if isinstance(resp_ps, str) and resp_ps.startswith('i'):
            resp_ps = resp_ps[1:]
            ipsi = True
            # print("Secondary response in primary site: ", sr_ps)
            # for each secondary response, check which other sites have this response as their primary response
        for secondary_site in range(len(df)):
            for response in range (9, 14):
                ss_index = secondary_site
                resp_ss = df.iloc[secondary_site, response]
                if (resp_ps == resp_ss):
                    w = calculate_weight(ps_index, ss_index)
                    buffer.append(w)

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
    

#print("WEIGHT", site+1, weight)

ri_array = np.array(ri_array)
ri_array = ri_array/(np.max(ri_array))
print(ri_array)

c.colorize(ri_array, "ri_penfield")