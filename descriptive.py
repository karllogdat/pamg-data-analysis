import pandas as pd
from math import log2

harmoni_df = pd.read_csv('harmoni.csv')
baseline_df = pd.read_csv('baseline.csv')

baseline_df.loc[baseline_df['Preset'] == 'A', 'Preset'] = 'Q1'
baseline_df.loc[baseline_df['Preset'] == 'B', 'Preset'] = 'Q2'
baseline_df.loc[baseline_df['Preset'] == 'C', 'Preset'] = 'Q3'
baseline_df.loc[baseline_df['Preset'] == 'D', 'Preset'] = 'Q4'

# convert raw pce values to 0-1 entropy values for easier interpretation
harmoni_df['Pitch_Class_Entropy'] /= log2(12)
baseline_df['Pitch_Class_Entropy'] /= log2(12)

harmoni_mean_key_corr_df = harmoni_df.groupby('Preset').agg(Average_Correlation=('Correlation', 'mean'))
baseline_mean_key_corr_df = baseline_df.groupby('Preset').agg(Average_Correlation=('Correlation', 'mean'))
combined_mean_key_corr_df = pd.concat(
    [
        harmoni_mean_key_corr_df.rename(columns={'Average_Correlation': 'Mean_Harmoni'}),
        baseline_mean_key_corr_df.rename(columns={'Average_Correlation': 'Mean_Baseline'})
    ],
    axis=1
)

# print("\n===== Mean Key Correlation =====")
# print(combined_mean_key_corr_df)

harmoni_mean_pce_df = harmoni_df.groupby('Preset').agg(Average_PCE=('Pitch_Class_Entropy', 'mean'))
baseline_mean_pce_df = baseline_df.groupby('Preset').agg(Average_PCE=('Pitch_Class_Entropy', 'mean'))
combined_mean_pce_df = pd.concat(
    [
        harmoni_mean_pce_df.rename(columns={'Average_PCE': 'Mean_Harmoni'}),
        baseline_mean_pce_df.rename(columns={'Average_PCE': 'Mean_Baseline'})
    ],
    axis=1
)

# print("\n===== Mean Pitch Class Entropy =====")
# print(combined_mean_pce_df)

harmoni_sd_key_corr_df = harmoni_df.groupby('Preset').agg(SD_Correlation=('Correlation', 'std'))
baseline_sd_key_corr_df = baseline_df.groupby('Preset').agg(SD_Correlation=('Correlation', 'std'))
combined_sd_key_corr_df = pd.concat(
    [
        harmoni_sd_key_corr_df.rename(columns={'SD_Correlation': 'Harmoni'}),
        baseline_sd_key_corr_df.rename(columns={'SD_Correlation': 'Baseline'})
    ],
    axis=1
)

combined_mean_key_corr_df['SD_Harmoni'] = combined_sd_key_corr_df['Harmoni']
combined_mean_key_corr_df['SD_Baseline'] = combined_sd_key_corr_df['Baseline']

print("\n===== Key Correlation =====")
print(combined_mean_key_corr_df)

harmoni_sd_pce_df = harmoni_df.groupby('Preset').agg(SD_PCE=('Pitch_Class_Entropy', 'std'))
baseline_sd_pce_df = baseline_df.groupby('Preset').agg(SD_PCE=('Pitch_Class_Entropy', 'std'))
combined_sd_pce_df = pd.concat(
    [
        harmoni_sd_pce_df.rename(columns={'SD_PCE': 'Harmoni'}),
        baseline_sd_pce_df.rename(columns={'SD_PCE': 'Baseline'})
    ],
    axis=1
)

combined_mean_pce_df['SD_Harmoni'] = combined_sd_pce_df['Harmoni']
combined_mean_pce_df['SD_Baseline'] = combined_sd_pce_df['Baseline']

print("\n===== Pitch Class Entropy =====")
print(combined_mean_pce_df)