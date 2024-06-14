import pandas as pd
import plotly.graph_objects as go

# Read the CSV data from a file
file_path = r'C:\Users\ghuysn\ESTD_VUBxUCL_VF\EnergyScope_multi_criteria_VUBxUCL_VF\case_studies\Final_results\2\output\sankey\input2sankey.csv'  # Replace with your actual file path
df = pd.read_csv(file_path, delimiter=',')

# Generate node list
nodes = list(set(df['source']).union(set(df['target'])))

# Create node indices dictionary
node_indices = {node: i for i, node in enumerate(nodes)}

# Create a dictionary for source to layerColor mapping
color_mapping = df[['source', 'layerColor']].drop_duplicates().set_index('source')['layerColor'].to_dict()

# Function to convert hex color to RGBA with reduced opacity
def hex_to_rgba(hex_color, opacity=0.5):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f'rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {opacity})'

# Prepare data for Sankey diagram
def get_link_color(source):
    hex_color = color_mapping.get(source, '#006400')  # Default color if no match found
    return hex_to_rgba(hex_color)

sankey_data = dict(
    type='sankey',
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=nodes,
        color='grey',  # Setting node color to black or any single color as we are focusing on link colors
    ),
    link=dict(
        source=[node_indices[src] for src in df['source']],
        target=[node_indices[dst] for dst in df['target']],
        value=df['realValue'],
        color=[get_link_color(src) for src in df['source']]
    )
)

# Create figure
fig = go.Figure(data=[sankey_data])

# Update layout
fig.update_layout(title_text="Energy Flow Sankey Diagram", font_size=10)

# Show plot
fig.show()