from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value
import csv
import os

# Set building
K = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
I = ["Aircraft", "Fuel", "Employee"]
J = ["Passenger", "Freight"]

# Parameters building
X = { 
    i: {
        k: 0 for k in K
    } for i in I
}
Y = { 
    j: {
        k: 0 for k in K
    } for j in J
}

X = {}
for col in I:
    X[col] = df[col].to_dict()

Y = {}
for col in J:
    Y[col] = df[col].to_dict()

K = list(df.index.unique())

# Import CSV data
with open(os.getcwd() + '/DecisionScience/DEA/airlines_data.csv', newline='') as csvfile:
    rows = csv.DictReader(csvfile)
    k = 0
    for row in rows:
        for i in I:
            X[i][K[k]] = float(row[i]) 
        for j in J:
            Y[j][K[k]] = float(row[j])
        k += 1


# CRS_DEA_Model        
def getOverallEfficiency(r):

    # Model Building
    model = LpProblem('CRS_model', LpMinimize) # 建立一個新的model，命名為model
    
    # Decision variables Building
    theta_r = LpVariable(f'theta_r')
    lambda_k = LpVariable.dicts(f'lambda_k', lowBound=0, indexs=K)
    
    # Objective Function setting
    model += theta_r
    
    # Constraints setting
    for i in I:
        model += lpSum([
                lambda_k[k] * X[i][k]
            for k in K]) <= theta_r * float(X[i][K[r]])
    for j in J:
        model += lpSum([
                lambda_k[k] * Y[j][k]
            for k in K]) >= float(Y[j][K[r]])
    
    # Model solving
    model.solve()
    
    return f'{K[r]}：{round(value(model.objective), 3)}\n', value(model.objective)

# VRS_DEA_Model
def getTechnicalEfficiency(r):

    # Model Building 
    model = LpProblem('VRS_model', LpMinimize) # 建立一個新的model，命名為model
    
    # Decision variables Building 
    theta_r = LpVariable(f'theta_r')
    lambda_k = LpVariable.dicts(f'lambda_k', lowBound=0, indexs = K)
    
    # Objective Function setting
    model += theta_r
    
    # Constraints setting
    for i in I:
        model += lpSum([
                lambda_k[k] * X[i][k]
            for k in K]) <= theta_r * float(X[i][K[r]])
    for j in J:
        model += lpSum([
                lambda_k[k] * Y[j][k]
            for k in K]) >= float(Y[j][K[r]])
    model += lpSum([ lambda_k[k] for k in K]) == 1
    
    # model solving 
    model.solve()  
    
    return f'{K[r]}：{round(value(model.objective), 3)}\n', value(model.objective)


OE_outputText = 'These are OE of all DMUs\n-------------\n'
TE_outputText = 'These are TE of all DMUs\n-------------\n'
SE_outputText = 'These are SE of all DMUs\n-------------\n'

for k in range(len(K)):
    OE_text, OE_val = getOverallEfficiency(k)
    #TE_text, TE_val = getTechnicalEfficiency(k)
    OE_outputText += OE_text
    #TE_outputText += TE_text
    #SE_outputText += f'{K[k]}：{round(OE_val / TE_val, 3)}\n'
print(OE_outputText)
#print(TE_outputText)
#print(SE_outputText)