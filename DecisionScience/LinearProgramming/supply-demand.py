import pulp as p
import pandas as pd
import math
from natsort import natsort_keygen
import warnings
warnings.filterwarnings("ignore")

solver_list = p.listSolvers(onlyAvailable=True)

print("The solver used in solving this Linear Programming problem: ", solver_list[0])

# ///*************** DATA INPUT ***************\\\
origin_df = pd.read_excel('Input excel files/Origins.xlsx')
origin_df.columns = ['ID', 'Latitude', 'Longitude', 'M1', 'M2', 'M3']

destinations_df = pd.read_excel('Input excel files/Destinations.xlsx')

origins = origin_df['ID']
destinations = destinations_df['ID']
materials = ['M1', 'M2', 'M3']

# ///*************** FUNCTION TO CALCULATE HAVERSINE DISTANCE BETWEEN TWO POINTS ***************\\\
def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Radius of Earth in kilometers
    R = 6371.0
    distance = R * c

    return distance

# ///*************** CREATE DISTANCE MATRIX ***************\\\
distances = []
routes = []
for idx in range(len(origin_df)):
    lon1 = origin_df.loc[idx, 'Longitude']
    lat1 = origin_df.loc[idx, 'Latitude']
    for idx2 in range(len(destinations_df)):
        lon2 = destinations_df.loc[idx2, 'Longitude']
        lat2 = destinations_df.loc[idx2, 'Latitude']
        try:
            distance = haversine(lat1, lon1, lat2, lon2)
            distances.append(distance)
            routes.append((origin_df.loc[idx, 'ID'], destinations_df.loc[idx2, 'ID']))
        except:
            print(origin_df.loc[idx, 'ID'])
            print(destinations_df.loc[idx2, 'ID'])

distance_matrix = pd.DataFrame([routes,distances]).T
distance_matrix.columns = ['route','km']
distance_km = distance_matrix.set_index('route').to_dict()['km']

# ///*************** CREATE SUPPLY DICTIONARY ***************\\\
supply = origin_df[['ID', 'M1', 'M2', 'M3']].set_index('ID').T.to_dict()

# ///*************** CREATE DEMAND DICTIONARY ***************\\\
demand_total = dict(zip(destinations_df['ID'], destinations_df['Required quantity']))

#  ///*************** INITIATE LP MINIMISATION PROBLEM ***************\\\
Lp_prob = p.LpProblem('Problem', sense = p.LpMinimize)  


#  ///*************** DEFINE DECISION VARIABLES x: EACH MATERIAL LOAD TRANSPORTED BETWEEN PAIR OF POINTS ***************\\\
x = p.LpVariable.dicts("transport", 
                          [(o, d, m) for o in origins for d in destinations for m in materials], 
                          lowBound=0,
                          cat='Continuous')

#  ///*************** DEFINE DECISION VARIABLES y: BLENDING OPTION AT EACH DESTINATION ***************\\\
y = p.LpVariable.dicts("y", 
                    [(d, option) for d in destinations for option in ['M2', 'M3']], 
                          cat='Binary')

# ///*************** OBJECTIVE FUNCTION: MINIMISE TRANSPORTATION COST ***************\\\
pertonkm_cost = 8.24
Lp_prob += p.lpSum([pertonkm_cost * distance_km[(o, d)] * x[o, d, m] for o in origins for d in destinations for m in materials])

# ///*************** CONSTRAINTS: CAN'T SUPPLY MORE THAN AVAILABLE ***************\\\
for o in origins:
    for m in materials:
        Lp_prob += p.lpSum([x[o, d, m] for d in destinations]) <= supply[o][m], f"Supply_Constraint_{o}_{m}"

# ///*************** CONSTRAINTS: BLENDING AT EACH DESTINATION ***************\\\
for d in destinations:
    Lp_prob += p.lpSum([x[o, d, 'M1'] for o in origins]) == 0.05 * demand_total[d], f"Demand_Constraint_M1_{d}"
    Lp_prob += p.lpSum([x[o, d, 'M2'] for o in origins]) == 0.10 * demand_total[d] * y[d, 'M2'], f"Demand_Constraint_M2_{d}"
    Lp_prob += p.lpSum([x[o, d, 'M3'] for o in origins]) == 0.20 * demand_total[d] * y[d, 'M3'], f"Demand_Constraint_M3_{d}"
    Lp_prob += y[d, 'M2'] + y[d, 'M3'] == 1, f"Blending_Option_Selection_{d}" # This will ensure that each destination either receives M2 or M3

 # ///*************** SOLVE LP PROBLEM ***************\\\
Lp_prob.solve()
print(f"Status: {p.LpStatus[Lp_prob.status]}")
print("Total Cost = ", p.value(Lp_prob.objective))


 # ///*************** RESULTS ***************\\\
distance_matrix[['SupplyPoint', 'DemandPoint']] = pd.DataFrame(distance_matrix['route'].tolist(), index=distance_matrix.index)
import regex as re

loads = []
routes = []
for v in Lp_prob.variables():
    if 'trans' in v.name:
        routes.append(re.findall(r"transport_\('([^']*)',_'([^']*)',_'([^']*)'\)", v.name)[0])
        loads.append(v.varValue)

loads_matrix = pd.DataFrame([routes,loads]).T
loads_matrix.columns = ['route','load']

loads_matrix[['SupplyPoint', 'DemandPoint', 'Material']] = pd.DataFrame(loads_matrix['route'].tolist(), index=loads_matrix.index)

finalresults = loads_matrix.merge(distance_matrix, on=['SupplyPoint','DemandPoint'])
finalresults['Cost'] = finalresults['load']*finalresults['km']*pertonkm_cost
finalresults = finalresults[['SupplyPoint', 'DemandPoint', 'Material', 'load', 'km', 'Cost']]

finalresults[finalresults.load != 0].sort_values(['DemandPoint','SupplyPoint'],key=natsort_keygen()).to_excel('final_results.xlsx', index=False)

supplied = finalresults.groupby(['SupplyPoint','Material'])[['load']].sum().reset_index()
supplied = supplied.pivot_table(index='SupplyPoint',columns='Material',values='load').reset_index()
merged_df = pd.merge(supplied, origin_df, left_on='SupplyPoint', right_on='ID', suffixes=('_df1', '_df2'))
# List of columns to compare
metrics = ['M1', 'M2', 'M3']

# Calculate differences
for metric in metrics:
    merged_df[f'{metric}_diff'] = merged_df[f'{metric}_df2'] - merged_df[f'{metric}_df1']

# Drop the original columns --  only want the differences
result_df = merged_df[['ID'] + [f'{metric}_diff' for metric in metrics]]
result_df['M1_diff'] = result_df['M1_diff']
result_df['M2_diff'] = result_df['M2_diff']
result_df['M3_diff'] = result_df['M3_diff']

result_df.sort_values(['ID'],key=natsort_keygen()).to_excel('leftover_surplus.xlsx', index=False)