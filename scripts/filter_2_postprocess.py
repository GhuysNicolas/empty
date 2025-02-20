import pandas as pd

# Define file paths
assets_file_path = r'/case_studies/FEDECOM/D3.3_FINAL_RESULTS/CH_B3/output/lca_breakdown.txt'  # Path to your assets file
selection_file_path = 'selection.txt'  # Path to your selection list file
output_file_path = 'filtered_assets.txt'  # Path to save the filtered data

# Load the assets data into a dataframe
assets_df = pd.read_csv(assets_file_path, sep='\t')

# Load the selection list
with open(selection_file_path, 'r') as file:
    selection_list = file.read().splitlines()

# Filter the dataframe to keep only the rows where the TECHNOLOGIES column matches the selection list
filtered_assets_df = assets_df[assets_df['Name'].isin(selection_list)]

# Save the filtered dataframe to a new file
filtered_assets_df.to_csv(output_file_path, sep='\t', index=False)

print(f"Filtered data has been saved to {output_file_path}")
