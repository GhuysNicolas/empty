import pandas as pd
import plotly.graph_objects as go

# Read the CSV data from a file
file_path = 'input2sankey.csv'  # Replace with your actual file path
df = pd.read_csv(file_path, delimiter=',')

# Generate node list
nodes = list(set(df['source']).union(set(df['target'])))

# Create node indices dictionary
node_indices = {node: i for i, node in enumerate(nodes)}

# Create a dictionary for source to layerColor mapping
color_mapping = df[['source', 'layerColor']].drop_duplicates().set_index('source')['layerColor'].to_dict()

# Prepare data for Sankey diagram
def get_node_color(node):
    # First check if the node exists in the source color mapping
    if node in color_mapping:
        return color_mapping[node]
    # If not found, check in the target columns as targets might not have color in source mapping
    target_color = df.loc[df['target'] == node, 'layerColor']
    if not target_color.empty:
        return target_color.values[0]
    # Default color if no match found
    return '#006400'

sankey_data = dict(
    type='sankey',
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=nodes,
        color=[get_node_color(node) for node in nodes],
    ),
    link=dict(
        source=[node_indices[src] for src in df['source']],
        target=[node_indices[dst] for dst in df['target']],
        value=df['realValue']
    )
)

# Create figure
fig = go.Figure(data=[sankey_data])

# Update layout
fig.update_layout(title_text="Energy Flow Sankey Diagram", font_size=10)

# Show plot
fig.show()
