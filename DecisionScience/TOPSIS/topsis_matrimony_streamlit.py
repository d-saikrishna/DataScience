import streamlit as st
from topsis import Topsis
import pandas as pd
import numpy as np 
import os

st.write("# Whom to marry?")
st.write("### Your father got you profiles of 20 men who want to marry you:")

current_path = os.getcwd()+'/DecisionScience/TOPSIS/'
matrimony_df = pd.read_csv(current_path + 'potential_grooms.csv')
matrimony_df = st.data_editor(matrimony_df, num_rows = "dynamic")

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

evaluation_matrix = np.array(matrimony_df.iloc[:,1:].values)

weight_salary = st.sidebar.slider(label="Weightage for Salary", min_value=1, max_value=3, value=3)
weight_wealth = st.sidebar.slider(label="Weightage for Wealth", min_value=1, max_value=3, value=3)
weight_siblings = st.sidebar.slider(label="Weightage for Siblings", min_value=1, max_value=3, value=3)
weight_complexion = st.sidebar.slider(label="Weightage for Complexion", min_value=1, max_value=3, value=3)
weight_height = st.sidebar.slider(label="Weightage for Height", min_value=1, max_value=3, value=3)
weight_bmi = st.sidebar.slider(label="Weightage for BMI", min_value=1, max_value=3, value=3)

weights = [weight_salary,
           weight_wealth,
           weight_siblings,
           weight_complexion,
           weight_height,
           weight_bmi] #Equal weights to all variables

criterias = [True, True, True, True, True, False]
# All variables - more is better; Except "dist_Ideal_BMI" which is lower the better

t = Topsis(evaluation_matrix, weights, criterias)

t.calc()
matrimony_df['TOPSIS_Score'] = t.worst_similarity

matrimony_df = matrimony_df.sort_values(by='TOPSIS_Score', ascending=False)

matrimony_df["Siblings"]=matrimony_df["Siblings"].replace([0, 1],["Yes","No"])
matrimony_df["Complexion"]=matrimony_df["Complexion"].replace([3,2,1],["Fair", "Wheatish", 'Dark'])

st.write("### TOPSIS suggested top 3 choices of grooms are:")
st.write(matrimony_df.head(3))

st.write("Change weightages in the sidebar to suit your value system")

st.write("PS: For the purposes of quantification, fairer complexion and lack of siblings is treated as 'better'.")
