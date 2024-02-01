import pandas as pd 
import os
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

assam_antyodaya_2020_df  = pd.read_csv(os.getcwd() + '/data/Assam_Antyodaya_2020.csv')

path = os.getcwd() + '/Unsupervised/PCA/'
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


# PCA
selected_vars = ['pct_0_3_anganwadi', 'pct_0_3_immunised',
    'pct_0_6_underweight', 'pct_0_6_anaemia',
    'pct_0_6_immunised']

pca = PCA(n_components = 5)
X = pca.fit_transform(child_df[vars])
principalDf = pd.DataFrame(data = X,
                           columns = ['PC1', 'PC2', 'PC3', 'PC4', 'PC5'])
principalDf.index = child_df['village_code']

# SCREE PLOT
explained_variance = pca.explained_variance_ratio_
print(explained_variance)

PC_values = np.arange(pca.n_components_) + 1
plt.plot(PC_values, explained_variance, 'o-', linewidth=2, color='blue')
plt.title('Scree Plot')
plt.xlabel('Principal Component')
plt.ylabel('Variance Explained')
plt.savefig(path + 'screeplot.jpg')

# LOADINGS
loadings = pca.components_
print(loadings)


# PC SCATTER PLOT
principalDf['pct_0_6_immunised'] = child_df['pct_0_6_immunised'].to_list()
sns.scatterplot(data=principalDf, x="PC1", y="PC2", hue='pct_0_6_immunised')
plt.savefig(path + 'scatter.jpg')


# BIPLOT
fig, ax = plt.subplots(figsize=(14, 9))
PC1 = principalDf['PC1']
PC2 = principalDf['PC2']
scalePC1 = 1.0/(PC1.max() - PC1.min())
scalePC2 = 1.0/(PC2.max() - PC2.min())

for i, feature in enumerate(vars):
    ax.arrow(0, 0, loadings[0, i], 
             loadings[1, i])
    ax.text(loadings[0, i] * 1.15, 
            loadings[1, i] * 1.15, 
            feature, fontsize=18)
 
ax.scatter(PC1 * scalePC1,PC2 * scalePC2)
 
ax.set_xlabel('PC1', fontsize=20)
ax.set_ylabel('PC2', fontsize=20)
ax.set_title('Figure 1', fontsize=20)
plt.savefig(path + 'biplot.jpg')