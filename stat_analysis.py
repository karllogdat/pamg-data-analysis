import pandas as pd
from scipy import stats

import matplotlib.pyplot as plt

harmoni_df = pd.read_csv('harmoni.csv')
baseline_df = pd.read_csv('baseline.csv')

pce_diff = harmoni_df['Pitch_Class_Entropy'] - baseline_df['Pitch_Class_Entropy']
stat_sw, p_sw = stats.shapiro(pce_diff)
print(f"Shapiro-Wilk Test for Normality: Statistic={stat_sw}, P-value={p_sw}")

zero_count = (pce_diff == 0).sum()
if zero_count > 0:
    print(f"Warning: {zero_count} zero differences found. Wilcoxon test may not be valid.")

stat, p_value = stats.wilcoxon(baseline_df['Pitch_Class_Entropy'], harmoni_df['Pitch_Class_Entropy'])
print(f"Total PCE Difference (Wilcoxon)::Statistic: {stat}, P-value: {p_value}")