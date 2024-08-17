import pandas as pd
import plotly.graph_objects as go
import plotly

df = pd.read_excel("final_results.xlsx")

# Summing weights by Source, Destination, and Material
grouped_df = df.groupby(['SupplyPoint', 'DemandPoint', 'Material']).sum().reset_index()

# Creating labels for Sankey nodes
all_labels = list(pd.concat([grouped_df['SupplyPoint'], grouped_df['DemandPoint'], grouped_df['Material']]).unique())
label_to_index = {label: index for index, label in enumerate(all_labels)}

# Preparing Sankey components
source_indices = [label_to_index[src] for src in grouped_df['SupplyPoint']]
destination_indices = [label_to_index[dest] for dest in grouped_df['DemandPoint']]
material_indices = [label_to_index[mat] for mat in grouped_df['Material']]

# Plotting the Sankey diagram
fig = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=all_labels,
    ),
    link=dict(
        source=source_indices,
        target=destination_indices,
        value=grouped_df['load']
    )
))

fig.update_layout(title_text="Sankey Diagram: Material Transport", font_size=10)

# Save the figure
file_path = 'sankey_offline.html'
plotly.offline.plot(fig, filename=file_path)