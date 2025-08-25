# -*- coding: utf-8 -*-
"""
Created on 2025/8/1 22:33

@author: starry
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import statsmodels.api as sm

# Read CSV files
df = pd.read_csv("/Users/starry/Documents/GIS/Applied Project(Academic)/Picture1/5 min BusStops Accessibility Index.csv")

# Extract the fields that need to be analyzed
x = df["Accessibility Index"]
y = df["Income Rank"]

# Delete missing values
data = pd.DataFrame({"Accessibility Index": x, "Income Rank": y}).dropna()
x_clean = data["Accessibility Index"]
y_clean = data["Income Rank"]

# Visualization: Scatter plot + regression line
plt.figure(figsize=(8, 6))
sns.regplot(x=x_clean, y=y_clean, line_kws={"color": "red"}, scatter_kws={"color": "blue"})
plt.xlabel("Accessibility Index")
plt.ylabel("Income Rank")
plt.title("Relationship Between Accessibility Index and Income Rank")
plt.grid(True)
plt.tight_layout()
plt.show()

# Pearson's correlation coefficient
corr, p_value = pearsonr(x_clean, y_clean)
print(f"Pearson's correlation coefficient: {corr:.3f}")
print(f"p 值: {p_value:.5f}")

# linear regression model
X = sm.add_constant(x_clean)
model = sm.OLS(y_clean, X).fit()
print(model.summary())