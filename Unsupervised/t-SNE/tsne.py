import pandas as pd 
import os
import numpy as np
from sklearn.manifold import TSNE
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

assam_antyodaya_2020_df  = pd.read_csv(os.getcwd() + '/data/Assam_Antyodaya_2020.csv')

path = os.getcwd() + '/Unsupervised/t-SNE/'
# Considering columns related to children <6 years
columns_to_consider = ['village_code', 'total_childs_aged_0_to_3_years',
                       'total_childs_aged_0_to_3_years_reg_under_aanganwadi',
                        'total_childs_aged_3_to_6_years_reg_under_aanganwadi',
                        'total_childs_aged_0_to_3_years_immunized',
                        'total_childs_categorized_non_stunted_as_per_icds',
                        'total_underweight_child_age_under_6_years',
                        'total_male_child_age_bw_0_6',
                        'total_female_child_age_bw_0_6',
                        'total_no_of_registered_children_in_anganwadi',
                        'total_no_of_children_0_to_6_years_immunized_under_icds',
                        'total_no_of_young_anemic_children_6_59_months_in_icds_cas']

assam_antyodaya_2020_df_children = assam_antyodaya_2020_df[columns_to_consider]

# Based on this data, let's find clusters of villages in Assam that are performing poorly for children

# FEATURE ENGINEERING
assam_antyodaya_2020_df_children['total_child_age_bw_0_6'] = assam_antyodaya_2020_df_children['total_female_child_age_bw_0_6'] + assam_antyodaya_2020_df_children['total_male_child_age_bw_0_6']

assam_antyodaya_2020_df_children['pct_0_3_anganwadi'] = assam_antyodaya_2020_df_children['total_childs_aged_0_to_3_years_reg_under_aanganwadi']/assam_antyodaya_2020_df_children['total_childs_aged_0_to_3_years']
assam_antyodaya_2020_df_children['pct_0_3_immunised'] = assam_antyodaya_2020_df_children['total_childs_aged_0_to_3_years_immunized']/assam_antyodaya_2020_df_children['total_childs_aged_0_to_3_years']

assam_antyodaya_2020_df_children['pct_0_6_underweight'] = assam_antyodaya_2020_df_children['total_underweight_child_age_under_6_years']/assam_antyodaya_2020_df_children['total_child_age_bw_0_6']
assam_antyodaya_2020_df_children['pct_0_6_anaemia'] = assam_antyodaya_2020_df_children['total_no_of_young_anemic_children_6_59_months_in_icds_cas']/assam_antyodaya_2020_df_children['total_child_age_bw_0_6']
assam_antyodaya_2020_df_children['pct_0_6_immunised'] = assam_antyodaya_2020_df_children['total_no_of_children_0_to_6_years_immunized_under_icds']/assam_antyodaya_2020_df_children['total_child_age_bw_0_6']

child_df = assam_antyodaya_2020_df_children[['village_code','pct_0_3_anganwadi', 'pct_0_3_immunised',
                                             'pct_0_6_underweight', 'pct_0_6_anaemia',
                                             'pct_0_6_immunised']]

# Let's ignore all villages without data for now
child_df = child_df.dropna()


# VARIATION
vars = ['pct_0_3_anganwadi', 'pct_0_3_immunised',
        'pct_0_6_underweight', 'pct_0_6_anaemia',
        'pct_0_6_immunised']

scaler = MinMaxScaler()
child_df_scaled = scaler.fit_transform(child_df[vars])
child_df_scaled = pd.DataFrame(data = child_df_scaled,
                           columns = vars)

for var in vars:
    variance = np.var(child_df_scaled[var])
    print('Variance of {}: {}'.format(var, round(variance, 2)))


# t-SNE
selected_vars = ['pct_0_3_anganwadi', 'pct_0_3_immunised',
    'pct_0_6_underweight', 'pct_0_6_anaemia',
    'pct_0_6_immunised']

m = TSNE(n_components=2, perplexity=30)
tsne_features = m.fit_transform(child_df[vars])
child_df['x'] = tsne_features[:,0]
child_df['y'] = tsne_features[:,1]

# SCATTER PLOT
sns.scatterplot(data=child_df, x="x", y="y", hue='pct_0_3_immunised')
plt.savefig(path + 'scatter.jpg')