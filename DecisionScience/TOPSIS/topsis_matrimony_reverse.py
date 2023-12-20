from topsis import Topsis
import pandas as pd
import numpy as np 
import os
import psweep as ps
import seaborn as sns
import matplotlib.pyplot as plt


current_path = os.getcwd()+'/DecisionScience/TOPSIS/'


def calculate_topsis(pset):
    matrimony_df = pd.read_csv(current_path + 'potential_grooms.csv')

    # More siblings is bad
    matrimony_df["Siblings"]=matrimony_df["Siblings"].replace(["Yes", "No"],[0,1])

    # Fairer the better
    matrimony_df["Complexion"]=matrimony_df["Complexion"].replace(["Fair", "Wheatish", 'Dark'],[3,2,1])

    # Feature Engineering - BMI
    matrimony_df["BMI"] = 10000*matrimony_df["Weight"]/(matrimony_df["Height"]**2)

    # BMI is not a variable that can be defined as "higher the better" - Considering 22 as ideal BMI
    matrimony_df["dist_ideal_BMI"] = abs(matrimony_df["BMI"]-22)

    # Dropping Weight and BMI
    matrimony_df = matrimony_df.drop(['BMI','Weight'], axis=1)

    evaluation_matrix = np.array(matrimony_df.iloc[:,1:].values) #ID not needed

    criterias = [True, True, True, True, True, False]
    # All variables - more is better; Except "dist_Ideal_BMI" which is lower the better 
    weights = [pset["weight_salary"], pset["weight_wealth"], pset["weight_sibling"],
               pset["weight_complexion"], pset["weight_height"], pset["weight_bmi"]]
    
    

    t = Topsis(evaluation_matrix, weights, criterias)
    t.calc()
    return {"topsis_score": t.worst_similarity[1],
            "topsis_rank": t.rank_to_worst_similarity()[1]}



#weights = [1, 1, 1, 1, 1, 1] #Equal weights to all variables

weights = np.arange(1,4,1)
weight_salary = ps.plist("weight_salary", weights)
weight_wealth = ps.plist("weight_wealth", weights)
weight_sibling = ps.plist("weight_sibling", weights)
weight_complexion = ps.plist("weight_complexion", weights)
weight_height = ps.plist("weight_height", weights)
weight_bmi = ps.plist("weight_bmi", weights)


params = ps.pgrid(weight_salary,
                  weight_wealth,
                  weight_sibling,
                  weight_complexion,
                  weight_height,
                  weight_bmi,
                  )

#params = ps.pgrid(weight_salary,weight_complexion,weight_wealth, weight_height,weight_bmi,weight_sibling)
print(len(params))

df = ps.run(calculate_topsis, params)

print(df[df['topsis_rank']==1].sort_values(by='topsis_score', ascending=False).head(1)[['weight_salary',
                  'weight_wealth',
                  'weight_sibling',
                  'weight_complexion',
                  'weight_height',
                  'weight_bmi',
                  'topsis_rank',
                  'topsis_score']])

df = df[df['_run_seq'] == df['_run_seq'].max()]

df = df[df['topsis_rank'] ==1]

df = df[['weight_salary',
         'weight_wealth',
         'weight_sibling',
         'weight_complexion',
         'weight_height',
         'weight_bmi']]

# Create an empty DataFrame to store value counts
value_counts_df = pd.DataFrame()

# Get value counts for each column and concatenate into the new DataFrame
for column in df.columns:
    value_counts = df[column].value_counts()
    value_counts_df = pd.concat([value_counts_df, value_counts], axis=1, sort=False)

# Fill NaN values with 0
value_counts_df = value_counts_df.fillna(0)

# Rename columns for clarity
value_counts_df.columns = [f'{col}' for col in df.columns]

# Create a heatmap using seaborn
plt.figure(figsize=(10, 6))
sns.heatmap(value_counts_df, annot=True, cmap='mako_r', fmt='g', linewidths=.5)
plt.title('Value Counts Heatmap')
plt.tight_layout()  # Adjust layout to prevent label cutoff
plt.xticks(rotation=0)
plt.savefig(current_path + 'psweep.jpg')