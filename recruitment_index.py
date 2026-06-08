import numpy as np
import pandas as pd

# =========================
# LOAD DATA
# =========================

df_pos = pd.read_excel(
    '/Users/felipepicard/Documents/01- Fisiologia da Cognição/03- Experimentos/01 - Mapeamento Motor Callithrix/CS-06/data/pos_teste.xlsx',
    sheet_name='pos'
)

df_meic = pd.read_excel(
    '/Users/felipepicard/Documents/01- Fisiologia da Cognição/03- Experimentos/01 - Mapeamento Motor Callithrix/CS-06/data/meic_timestamps_teste.xlsx',
    sheet_name='Timestamps_min'
)

# =========================
# CONFIG
# =========================

scale = 1
ipsi_factor = 1.3

secondary_cols = ['m1', 'm2', 'm3', 'm4', 'm5']

# coluna que contém os nomes dos sítios na planilha meic
MEIC_SITE_COLUMN = 'site'

# usar média das representações
get_mean_of_representations = False

# normalizar IRM
normalize_irm = False

# =========================
# FUNCTIONS
# =========================

def invalido(v):
    """
    Verifica se o valor é inválido/vazio.
    """

    return pd.isna(v) or str(v).strip().lower() in ["-", "", "nan"]


def site_valido(site_index):
    """
    Verifica se o sítio possui:
    - coordenadas válidas
    - representação primária válida
    """

    x = df_pos.iloc[site_index, 1]
    y = df_pos.iloc[site_index, 2]
    rep = df_pos.iloc[site_index, 3]

    if invalido(x) or invalido(y) or invalido(rep):
        return False

    return True


def calculate_weight(ps, ss, ipsi=False):
    """
    Distância euclidiana entre dois sítios.
    """

    ps_x = df_pos.iloc[ps, 1]
    ps_y = df_pos.iloc[ps, 2]

    ss_x = df_pos.iloc[ss, 1]
    ss_y = df_pos.iloc[ss, 2]

    ps_pos = np.array((ps_x, ps_y))
    ss_pos = np.array((ss_x, ss_y))

    if ipsi:

        dist = np.linalg.norm(ps_pos - ss_pos) * scale * ipsi_factor

        print("dist ipsi =", dist)

    else:

        dist = np.linalg.norm(ps_pos - ss_pos) * scale

        print("dist =", dist)

    return dist


def get_secondary_responses(site_number):
    """
    Procura a linha '<site_number> ld'
    na planilha meic_timestamps.
    """

    site_name = f"{site_number} ld"

    row = df_meic[df_meic[MEIC_SITE_COLUMN] == site_name]

    if row.empty:
        return []

    row = row.iloc[0]

    responses = []

    for col in secondary_cols:

        if col in row:

            value = row[col]

            if not invalido(value):
                responses.append(str(value).strip())

    return responses


# =========================
# RECRUITMENT INDEX
# =========================

all_ri = []

for site in range(len(df_pos)):

    site_number = df_pos.iloc[site, 0]

    # =========================
    # INVALID SITES
    # =========================

    if not site_valido(site):

        print(f"Sítio {site_number} inválido -> pulando")

        # salva placeholder
        all_ri.append((site_number, "-"))

        print("___________________________________________________________________________")

        continue

    weight = []

    # resposta primária do sítio atual
    primary_response = str(df_pos.iloc[site, 3]).strip()

    # respostas secundárias do sítio ld
    secondary_responses = get_secondary_responses(site_number)

    print("Resposta primária para sítio", site_number, "=", primary_response)
    print("Respostas secundárias para sítio", site_number, "=", secondary_responses)
    print("")

    # =========================
    # LOOP THROUGH RESPONSES
    # =========================

    for sr_ps in secondary_responses:

        # maioria é contralateral
        ipsi = False

        buffer = []

        # =========================
        # IPSILATERAL CHECK
        # =========================

        if isinstance(sr_ps, str) and sr_ps.endswith('-i'):

            print("ipsi response:", sr_ps)

            sr_ps = sr_ps[:-2]

            ipsi = True

        # =========================
        # SEARCH MATCHING SITES
        # =========================

        for secondary_site in range(len(df_pos)):

            # pula sítios inválidos
            if not site_valido(secondary_site):
                continue

            pr_ss = str(df_pos.iloc[secondary_site, 3]).strip()

            if pr_ss == sr_ps:

                print(
                    "Calculando a distância entre",
                    site_number,
                    "e",
                    df_pos.iloc[secondary_site, 0]
                )

                w = calculate_weight(site, secondary_site, ipsi)

                # print("weight value =", w)

                buffer.append(w)

        # =========================
        # REPRESENTATION WEIGHT
        # =========================

        new_weight = 0

        if len(buffer) > 0:

            if get_mean_of_representations:

                # média dos sítios recrutados
                new_weight = sum(buffer) / len(buffer)
                print("Dividindo ", buffer, "por", len(buffer), "->", new_weight)

            else:

                # soma total dos sítios recrutados
                new_weight = sum(buffer)

        weight.append(new_weight)

    # =========================
    # FINAL RI
    # =========================

    ri = sum(weight)

    all_ri.append((site_number, ri))

    print(f"Recruitment Index {site_number}: {ri:.2f}")

    print("___________________________________________________________________________")


# =========================
# FINAL OUTPUT
# =========================

print("\n\n====================")
print("IRNs FINAIS")
print("====================\n")

# pega apenas valores numéricos válidos
valid_ri = [ri for _, ri in all_ri if isinstance(ri, (int, float))]

# =========================
# NORMALIZATION
# =========================

if normalize_irm and len(valid_ri) > 0:

    max_val = np.max(valid_ri)

    print("Max RI =", round(max_val, 4))
    print("")

else:

    max_val = 1

# =========================
# FINAL PRINT
# =========================

for site_number, ri in all_ri:

    # mantém placeholders
    if ri == "-":

        print("-")

    else:

        # normaliza se necessário
        if normalize_irm and max_val != 0:

            ri = ri / max_val

        print(f"{ri:.2f}")
