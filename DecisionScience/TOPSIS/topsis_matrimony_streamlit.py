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

evaluation_matrix = np.array(matrimony_df.iloc[:,1:].values)

weight_salary = st.sidebar.slider(label="Weightage for Salary", min_value=0, max_value=10, value=10)
weight_wealth = st.sidebar.slider(label="Weightage for Wealth", min_value=0, max_value=10, value=10)
weight_siblings = st.sidebar.slider(label="Weightage for Siblings", min_value=0, max_value=10, value=10)
weight_complexion = st.sidebar.slider(label="Weightage for Complexion", min_value=0, max_value=10, value=10)
weight_height = st.sidebar.slider(label="Weightage for Height", min_value=0, max_value=10, value=10)
weight_weight = st.sidebar.slider(label="Weightage for Weight", min_value=0, max_value=10, value=10)

weights = [weight_salary,
           weight_wealth,
           weight_siblings,
           weight_complexion,
           weight_height,
           weight_weight] #Equal weights to all variables

criterias = [True, True, True, True, True, True]
# All variables - more is better

t = Topsis(evaluation_matrix, weights, criterias)

t.calc()
matrimony_df['TOPSIS_Score'] = t.worst_similarity

matrimony_df = matrimony_df.sort_values(by='TOPSIS_Score', ascending=False)

st.write("### TOPSIS suggested top 3 choices of grooms are:")
st.write(matrimony_df.head(3))

st.write("Change weightages in the sidebar to suit your value system")

st.write("PS: For the purposes of quantification, fairer complexion and lack of siblings is treated as 'better'.")
