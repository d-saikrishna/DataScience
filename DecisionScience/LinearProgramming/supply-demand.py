import pulp as p
import pandas as pd
import math
import itertools
import numpy as np
import regex as re
from tqdm import tqdm
from natsort import natsort_keygen
import warnings
warnings.filterwarnings("ignore")

solver_list = p.listSolvers(onlyAvailable=True)

print("The solver used in solving this Linear Programming problem: ", solver_list[0])

# ///*************** DATA INPUT ***************\\\
origin_df = pd.read_excel('ORIGINS.xlsx')
origin_df.columns = ['ID', 'M1', 'M2', 'M3']

destinations_df = pd.read_excel('DESTINATIONS.xlsx')

origins = origin_df['ID']
destinations = destinations_df['ID']
materials = ['M1', 'M2', 'M3']

origin_df = origin_df.fillna(0)
destinations_df = destinations_df.fillna(0)


# ///*************** DISTANCE MATRIX ***************\\\
distance_matrix = pd.read_excel('distance matrix.xlsx')
distance_matrix = pd.melt(distance_matrix, id_vars=['Unnamed: 0'], value_vars = list(origins))
distance_matrix.columns = ['D','S','km']
distance_matrix['route'] = distance_matrix.apply(lambda row: (row['S'], row['D']), axis=1)

distance_km = distance_matrix.set_index('route').to_dict()['km']

# ///*************** CREATE SUPPLY DICTIONARY ***************\\\
supply = origin_df[['ID', 'M1', 'M2', 'M3']].set_index('ID').T.to_dict()

# ///*************** CREATE DEMAND DICTIONARY ***************\\\
demand_total = dict(zip(destinations_df['ID'], destinations_df['Required quantity']))

# ///*************** FUNCTION THAT SOLVES THE LP PROBLEM***************\\\
def minimise_costs_lp(origins, destinations, materials, pertonkm_cost, distance_km, supply, demand_total):
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
        Lp_prob += y[d, 'M2'] + y[d, 'M3'] == 1, f"Blending_Option_Selection_{d}"
    
    # ///*************** SOLVE LP PROBLEM ***************\\\
    status = Lp_prob.solve()
    cost = p.value(Lp_prob.objective)
    vars = Lp_prob.variables()
    return status, cost, vars

# ///*************** ITERATIVELY SOLVE LP FOR DIFFERENT DESTINATION COMBINATIONS***************\\\
pertonkm_cost = 8.24
## ALL DESTINATIONS SERVED
status, cost, vars = minimise_costs_lp(origins, destinations, materials, pertonkm_cost, distance_km, supply, demand_total)
if status == 1:
    print('Linear Programming problem solved by delivering to all destinations')
    print(cost)
else:
    problem_solved = 0
    num_destinations_to_drop = 1
    while problem_solved == 0:
        print('Dropping {} destinations'.format(num_destinations_to_drop))
        destinations_to_drop = list(itertools.combinations(range(len(destinations)), num_destinations_to_drop))
        costs = []
        dropped = []
        for dropped_destination in tqdm(destinations_to_drop):
            dropped.append(destinations[list(dropped_destination)].values)
            new_destinations = destinations.drop(index=list(dropped_destination))
            status, cost, vars = minimise_costs_lp(origins, new_destinations, materials, pertonkm_cost, distance_km, supply, demand_total)
            if status == 1:
                costs.append(cost)
            else:
                costs.append(np.nan)

        df = pd.DataFrame([dropped,costs]).T
        df.columns = ['dropped_destination', 'cost']
        
        if df['cost'].count() >0:
            problem_solved=1
        else:
            num_destinations_to_drop = num_destinations_to_drop + 1

    destinations_to_remove = list(df.sort_values(by='cost')['dropped_destination'].reset_index(drop=True)[0])
    print(destinations_to_remove)
    new_destinations = destinations[~destinations.isin(destinations_to_remove)].reset_index(drop=True)
    status, cost, vars = minimise_costs_lp(origins, new_destinations, materials, pertonkm_cost, distance_km, supply, demand_total)

 # ///*************** RESULTS ***************\\\
distance_matrix[['SupplyPoint', 'DemandPoint']] = pd.DataFrame(distance_matrix['route'].tolist(), index=distance_matrix.index)

loads = []
routes = []
for v in vars:
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