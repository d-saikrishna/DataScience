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

# Feature Engineering - BMI
matrimony_df["BMI"] = 10000*matrimony_df["Weight"]/(matrimony_df["Height"]**2)

# BMI is not a variable that can be defined as "higher the better" - Considering 22 as ideal BMI
matrimony_df["dist_ideal_BMI"] = abs(matrimony_df["BMI"]-22)

# Dropping Weight and BMI
matrimony_df = matrimony_df.drop(['BMI','Weight'], axis=1)

evaluation_matrix = np.array(matrimony_df.iloc[:,1:].values) #ID not needed

weights = [3, 1, 1, 1, 3, 1] #Equal weights to all variables

criterias = [True, True, True, True, True, False]
# All variables - more is better; Except "dist_Ideal_BMI" which is lower the better

t = Topsis(evaluation_matrix, weights, criterias)

t.calc()
matrimony_df['TOPSIS_Score'] = t.worst_similarity

matrimony_df = matrimony_df.sort_values(by='TOPSIS_Score', ascending=False)
print('Top 3 choices are:')
print(matrimony_df.head(3))
