import streamlit as st
from topsis import Topsis
import pandas as pd
import numpy as np 
import os
import psweep as ps
import seaborn as sns
import matplotlib.pyplot as plt
st.set_page_config(layout="wide", page_title="Groom Recommending Engine")


tab1, tab2 = st.tabs(["Groom Recommendation", "Test your decisions"])

with tab1:
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

with tab2:
    st.write("# Lets test your decisions")
    current_path = os.getcwd()+'/DecisionScience/TOPSIS/'
    grooms_df = pd.read_csv(current_path + 'potential_grooms1.csv')
    matrimony_df2 = grooms_df.copy()
    grooms_df = st.dataframe(grooms_df)

    # More siblings is bad    
    matrimony_df2["Siblings"]=matrimony_df2["Siblings"].replace(["Yes", "No"],[0,1])

    # Fairer the better
    matrimony_df2["Complexion"]=matrimony_df2["Complexion"].replace(["Fair", "Wheatish", 'Dark'],[3,2,1])

    # Feature Engineering - BMI
    matrimony_df2["BMI"] = 10000*matrimony_df2["Weight"]/(matrimony_df2["Height"]**2)

    # BMI is not a variable that can be defined as "higher the better" - Considering 22 as ideal BMI
    matrimony_df2["dist_ideal_BMI"] = abs(matrimony_df2["BMI"]-22)

    # Dropping Weight and BMI
    matrimony_df2 = matrimony_df2.drop(['BMI','Weight'], axis=1)

    evaluation_matrix = np.array(matrimony_df2.iloc[:,1:].values)

    with st.form("my_form"):
        options = tuple(matrimony_df2.name)

        option = st.selectbox(
        'Whom do you want to marry?',
        options)

        index_of_element = options.index(option)

        submitted = st.form_submit_button("Submit")

    def calculate_topsis(pset):
        criterias = [True, True, True, True, True, False]
        # All variables - more is better; Except "dist_Ideal_BMI" which is lower the better 
        weights = [pset["weight_salary"], pset["weight_wealth"], pset["weight_sibling"],
                pset["weight_complexion"], pset["weight_height"], pset["weight_bmi"]]
        
        t = Topsis(evaluation_matrix, weights, criterias)
        t.calc()
        return {"topsis_score": t.worst_similarity[index_of_element],
                "topsis_rank": t.rank_to_worst_similarity()[index_of_element]}
    
    weights = np.arange(1,4,1)
    weight_salary = ps.plist("weight_salary", weights)
    weight_wealth = ps.plist("weight_wealth", weights)
    weight_sibling = ps.plist("weight_sibling", weights)
    weight_complexion = ps.plist("weight_complexion", weights)
    weight_height = ps.plist("weight_height", weights)
    weight_bmi = ps.plist("weight_bmi", weights)

    if submitted:
        params = ps.pgrid(weight_salary,
                        weight_wealth,
                        weight_sibling,
                        weight_complexion,
                        weight_height,
                        weight_bmi,
                        )
        
        df = ps.run(calculate_topsis, params)
        df = df[df['_run_seq'] == df['_run_seq'].max()]

        df = df[df['topsis_rank'] ==1]
        st.write('### {} has {}% chance of getting selected'.format(option, round(100*df.shape[0]/len(params), 2) ))
        st.write('{} is most likely to be selected when: '.format(option))
        st.write(df.sort_values(by='topsis_score', ascending=False).head(1)[['weight_salary',
                'weight_wealth',
                'weight_sibling',
                'weight_complexion',
                'weight_height',
                'weight_bmi']])


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

        

        st.image(current_path + 'psweep.jpg')
    
