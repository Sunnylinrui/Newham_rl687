# -*- coding: utf-8 -*-
"""
Created on 2025/8/1 21:14

@author: starry
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import statsmodels.api as sm

# Read CSV files
df = pd.read_csv("/Users/starry/Documents/GIS/Applied Project(Academic)/Picture1/10 min Stations IMD & Income.csv")

# Extract the fields that need to be analyzed
x = df["Accessibility Index"]
y = df["Barriers to Housing and Services Score"]

# Delete missing values
data = pd.DataFrame({"Accessibility Index": x, "Barriers to Housing and Services Score": y}).dropna()
x_clean = data["Accessibility Index"]
y_clean = data["Barriers to Housing and Services Score"]

# Visualization: Scatter plot + regression line
plt.figure(figsize=(8, 6))
sns.regplot(x=x_clean, y=y_clean, line_kws={"color": "red"}, scatter_kws={"color": "orange"})
plt.xlabel("Accessibility Index")
plt.ylabel("Barriers to Housing and Services Score")
plt.title("Relationship Between Accessibility Index and Barriers to Housing and Services Score")
plt.grid(True)
plt.tight_layout()
plt.show()

# Pearson's correlation coefficient
corr, p_value = pearsonr(x_clean, y_clean)
print(f"Pearson's correlation coefficient: {corr:.3f}")
print(f"p : {p_value:.5f}")

# linear regression model
X = sm.add_constant(x_clean)
model = sm.OLS(y_clean, X).fit()
print(model.summary())