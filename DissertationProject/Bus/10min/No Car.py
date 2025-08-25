# -*- coding: utf-8 -*-
"""
Created on 2025/8/1 21:59

@author: starry
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import statsmodels.api as sm

# Read CSV files
df = pd.read_csv("/Users/starry/Documents/GIS/Applied Project(Academic)/Picture1/10 min BusStops Accessibility Index.csv")

# Extract the two columns that need to be analyzed
x = df['Accessibility Index']
y = df['No Car or vans in household(%)']

# Draw scatter plots and fit lines
plt.figure(figsize=(8, 6))
sns.regplot(x=x, y=y, line_kws={'color': 'red'})
plt.xlabel("Accessibility Index")
plt.ylabel("No Car or vans in household (%)")
plt.title("Relationship Between Accessibility and Car Ownership")
plt.grid(True)
plt.show()

# Calculate the Pearson correlation coefficient
corr, p_value = pearsonr(x, y)
print(f"Pearson's correlation coefficient: {corr:.3f}, p: {p_value:.5f}")

# linear regression model
X = sm.add_constant(x)
model = sm.OLS(y, X).fit()
print(model.summary())
