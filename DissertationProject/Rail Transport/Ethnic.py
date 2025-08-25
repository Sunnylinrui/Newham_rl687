# -*- coding: utf-8 -*-
"""
Created on 2025/8/1 19:47

@author: starry
"""
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# Read CSV files
file_path = "/Users/starry/Documents/GIS/Applied Project(Academic)/Picture1/Accessibility Index & Ethnic.csv"
df = pd.read_csv(file_path)

# Retain the relevant columns and delete the rows containing missing values
columns_of_interest = ['Accessibility Index', 'White British%', 'White%', 'Asian%', 'Black%']
df = df[columns_of_interest].dropna()

# Rename column names by removing Spaces and percent signs
df.columns = ['Accessibility', 'White_British', 'White', 'Asian', 'Black']

# Calculate the Pearson correlation coefficient and P-value
results = {}
for col in ['White_British', 'White', 'Asian', 'Black']:
    corr, p_val = stats.pearsonr(df['Accessibility'], df[col])
    results[col] = {'Pearson r': round(corr, 3), 'p-value': round(p_val, 3)}

# Convert to a DataFrame for display
results_df = pd.DataFrame(results).T
print(results_df)

# Draw a correlation heat map
plt.figure(figsize=(8, 6))
corr_matrix = df.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Accessibility Index & Ethnic Correlation Heatmap")
plt.tight_layout()
plt.show()