from topsis import Topsis
import pandas as pd
import numpy as np 
import os

current_path = os.getcwd()+'/DecisionScience/TOPSIS/'
matrimony_df = pd.read_csv(current_path + 'potential_grooms.csv')

# More siblings is bad
matrimony_df["Siblings"]=matrimony_df["Siblings"].replace(["Yes", "No"],[0,1])

# Fairer the better
matrimony_df["Complexion"]=matrimony_df["Complexion"].replace(["Fair", "Wheatish", 'Dark'],[3,2,1])

evaluation_matrix = np.array(matrimony_df.iloc[:,1:].values)

weights = [1, 1, 1, 1, 1, 1] #Equal weights to all variables

criterias = [True, True, True, True, True, True]
# All variables - more is better

t = Topsis(evaluation_matrix, weights, criterias)

t.calc()
matrimony_df['TOPSIS_Score'] = t.worst_similarity

matrimony_df = matrimony_df.sort_values(by='TOPSIS_Score', ascending=False)
print('Top 3 choices are:')
print(matrimony_df.head(3))
