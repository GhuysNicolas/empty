import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi

# Min and max values for each criterion
min_max_values = {
    'TotalCost': {'min': 43, 'max': 150},
    'LCA_tot': {'min': 0.0009, 'max': 120},
    'Acidification': {'min': 130, 'max': 700},
    'Land use': {'min': 100000, 'max': 3000000},
    'Water depletion': {'min': 10000, 'max': 300000}
}

# Function to read and format data
def read_and_format_data(filepath):
    data = []
    with open(filepath, 'r') as file:
        scenario = {}
        for line in file:
            if not line.strip():
                if scenario:
                    data.append(scenario)
                    scenario = {}
                continue
            key, value = line.strip().split()
            scenario[key] = float(value)
        if scenario:
            data.append(scenario)  # Add the last scenario

    df = pd.DataFrame(data)
    return df

# Function to normalize data based on provided min and max values
def normalize_data(df, min_max_dict):
    df_normalized = df.copy()
    for column in df.columns:
        min_val = min_max_dict[column]['min']
        max_val = min_max_dict[column]['max']
        df_normalized[column] = (df[column] - min_val) / (max_val - min_val)
    return df_normalized

# Function to create radar plot
def create_radar_plot(df, title, min_max_dict):
    # Normalize the data
    df = normalize_data(df, min_max_dict)

    # Number of variables
    categories = list(df.columns)
    N = len(categories)

    # What will be the angle of each axis in the plot
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)

    # Draw one axe per variable and add labels
    plt.xticks(angles[:-1], categories)

    # Plot data
    for i, row in df.iterrows():
        values = row.tolist()
        values += values[:1]
        ax.plot(angles, values, label=f'Objective {i + 1}')
        #ax.fill(angles, values, alpha=0.1)

    # Add a title
    plt.title(title, size=20, color='black', y=1.1)

    # Add a legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

    # Show the plot
    plt.show()

# Read and format data from the file
df = read_and_format_data('C:/Users/ghuysn/GIT_Projects/EnergyScope_LCA/case_studies/MC_outputs/MC_values.csv')

# Adjust the column names to match the min_max_values keys
df.columns = ['TotalCost','LCA_tot', 'Acidification', 'Land use', 'Water depletion']

# Create radar plot
create_radar_plot(df, 'Multi-Objective Optimisation', min_max_values)
